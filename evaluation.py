# Code for Evaluation
from BookKeeper import *
from WeightTrigger import WeightTrigger as WT
from utils import *
from cashier import Cashier
import json

"""
1. Evaluate inventory status
Metrics:
    1. Precision: TP/(TP+FP)
    2. Recall: TP/(TP+FN)
"""
def evaluate_intenvory(dbs=['cps-test-01'], gt_path='ground_truth/v9.json'):
    # Load JSON groundtruth
    with open(gt_path) as f:
        gt_data = json.load(f)

    gt_list = gt_data['lists']
    
    # Metrics 
    tp, fp, tn, fn = 0, 0, 0, 0
    overall_num_preds, overall_products = 0, 0
    for i in range(len(dbs)):
        print("Evaluating databse: ", dbs[i])
        ########## Generate Prediction ##########
        predicted_products = {}
        # Dictionary of all predicted products Key: ProductID Value: Quantity
        dbName = dbs[i]
        myCashier = Cashier()
        receipts = myCashier.process(dbName)
        num_preds = 0
        for _, customer_receipt in receipts.items():
            for _, entry in customer_receipt.purchaseList.items():
                product, quantity = entry
                productID = product.barcode
                if productID in predicted_products:
                    predicted_products[productID] += quantity
                else:
                    predicted_products[productID] = quantity
                num_preds += quantity
        print("Inventory Change in {}: ".format(dbName), predicted_products, " Amount: ", num_preds)

        ########## Evaluate Ground truth ##########
        num_events = 0
        num_products = 0
        num_correct_products = 0
        gt_entry = gt_list[i]
        # Find groundtruth entry for this database
        tmp_i = i
        while (gt_entry['dataset'] != dbName):
            tmp_i += 1 
            gt_entry = gt_list[tmp_i]
            assert (tmp_i<len(gt_list))
        assert (gt_entry['dataset'] == dbName)
        event_list = gt_entry['events']
        for event in event_list:
            num_events += 1
            products = event['observation']['products']
            for product in products:
                num_products += 1
                gt_productID = product['id']
                # Listed in our predicted receipts
                if (gt_productID in predicted_products and predicted_products[gt_productID] > 0):
                    predicted_products[gt_productID] -= 1
                    if (predicted_products[gt_productID] == 0):
                        del predicted_products[gt_productID]
                    tp += 1
                    num_correct_products += 1
                else:
                    fn += 1
                #     print("Product: ", num_products)
        for _, quantity in predicted_products.items():
            fp += quantity

        overall_num_preds += num_preds
        overall_products += num_products
        print("Detected products for {}: {}/{}, correct products {}".format(dbName, num_preds, num_products, num_correct_products))
    
    print("\n================== Evaluation Summary ==================")
    print("Databases: ", dbs)
    print("Ground truth version: ", gt_path)
    print("Overall products detection rate is: {:.1f}%".format(overall_num_preds*100.0 / overall_products))
    print("Overall precision is: {:.1f}%".format(tp*100.0 / (tp+fp)))
    print("Overall recall is: {:.1f}%".format(tp*100.0 / (tp+fn)))

if __name__ == "__main__":
    dbs=['cps-test-01', 'cps-test-2'] + ['cps-test-'+str(i) for i in range(4, 13)]
    gt_path='ground_truth/v9.json' # list of ground truth W.R.T the previous databses
    evaluate_intenvory(dbs, gt_path)