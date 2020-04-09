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
def evaluate_intenvory(dbs=['cps-test-01'], gt_paths=['ground_truth/v9.json']):
    assert (len(dbs) == len(gt_paths))
    for i in range(len(dbs)):
        # Load JSON groundtruth
        gt_path = gt_paths[i]
        with open(gt_path) as f:
            gt_data = json.load(f)

        gt_list = gt_data['lists']
        print("Length of ground truth: ", len(gt_list))

        ########## Generate Prediction ##########
        predicted_products = {}
        # Dictionary of all predicted products Key: ProductID Value: Quantity
        dbName = dbs[i]
        myCashier = Cashier()
        receipts = myCashier.process(dbName)
        for _, customer_receipt in receipts.items():
            for _, entry in customer_receipt.purchaseList.items():
                product, quantity = entry
                productID = product.barcode
                if productID in predicted_products:
                    predicted_products[productID] += quantity
                else:
                    predicted_products[productID] = quantity
        print("Inventory Change in prediction: ", predicted_products)

        ########## Evaluate Ground truth ##########
        num_events = 0
        num_products = 0
        tp, fp, tn, fn = 0, 0, 0, 0
        undetected = 0
        for gt_entry in gt_list:
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
                        tp += 1
                    else:
                        undetected += 1
                #     print("Product: ", num_products)
                # print("GT Event: ", num_events)
        print("Product detection rate: {:.2f}", (num_products - undetected)*1.0 / num_products)

if __name__ == "__main__":
    dbs=['cps-test-01'] # list of databases to evaluate
    gt_paths=['ground_truth/v9.json'] # list of ground truth W.R.T the previous databses
    evaluate_intenvory(dbs, gt_paths)