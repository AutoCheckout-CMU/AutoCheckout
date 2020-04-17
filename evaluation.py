# Code for Evaluation
from BookKeeper import *
from WeightTrigger import WeightTrigger as WT
from utils import *
from cashier import Cashier
import json

"""
Groundtruth file contains pickup event and putback event separately.
remove_putback_products() will remove the putback event as well as its coresponding pickup event,
so that the ground truth only contains file result. 
"""
def remove_putback_products(gt_list):
    for db in gt_list:
        final_events = []
        for event in db['events']:
            if event['putback'] == 0: # pick up
                final_events.append(event)
            else: # putback => remove from final_events the coresponding pickup event
                for i in range(len(final_events)):
                    final_event = final_events[i]
                    if final_event['observation']['target_id'] != event['observation']['target_id']:
                        continue 
                    if final_event['observation']['products'][0]['id'] != event['observation']['products'][0]['id']:
                        continue
                    del final_events[i]
        db['events'] = final_events

"""
1. Evaluate inventory status
Metrics:
    1. Precision: TP/(TP+FP)
    2. Recall: TP/(TP+FN)
2. Evaluate association accuracy
Metrics:
    1. Accuracy: num_correct_association/num_correct_products
"""
def evaluate_intenvory(dbs=['cps-test-01'], gt_path='ground_truth/v10.json'):
    # Load JSON groundtruth
    with open(gt_path) as f:
        gt_data = json.load(f)

    gt_list = gt_data['lists']
    if not DEBUG:
        remove_putback_products(gt_list)
        # with open('gt_final.json', 'w') as outfile:
        #     json.dump(gt_data, outfile)

    # Metrics 
    tp, fp, tn, fn = 0, 0, 0, 0
    tp_asso = 0
    overall_num_preds, overall_products = 0, 0
    for i in range(len(dbs)):
        print("Evaluating database: ", dbs[i])
        ########## Generate Prediction ##########
        predicted_products = {} # Dictionary of all predicted products Key: ProductID Value: Quantity
        dbName = dbs[i]
        myCashier = Cashier()
        receipts = myCashier.process(dbName)
        num_preds = 0
        for customerID, customer_receipt in receipts.items():
            for productID, entry in customer_receipt.purchaseList.items():
                product, quantity = entry
                if productID in predicted_products:
                    predicted_products[productID]['quantity'] += quantity
                else:
                    predicted_products[productID] = {'customerID': customerID, 'quantity': quantity}
                num_preds += quantity
        print("Inventory Change in {}: ".format(dbName), predicted_products, " Amount: ", num_preds)

        ########## Evaluate Ground truth ##########
        num_events = 0
        num_products = 0
        num_correct_products = 0
        num_correct_asso = 0
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
            gt_customerID = event['observation']['target_id']
            for product in products:
                num_products += 1
                gt_productID = product['id']
                ## Product
                # Listed in our predicted receipts
                if (gt_productID in predicted_products and predicted_products[gt_productID]['quantity'] > 0):
                    # print("GT Identity: ", gt_customerID, "Predicted: ", predicted_products[gt_productID]['customerID'])
                    if (predicted_products[gt_productID]['customerID'] == gt_customerID):
                        tp_asso += 1
                        num_correct_asso += 1
                    predicted_products[gt_productID]['quantity'] -= 1
                    if (predicted_products[gt_productID]['quantity'] == 0):
                        del predicted_products[gt_productID]
                    tp += 1
                    num_correct_products += 1
                else:
                    fn += 1
                #     print("Product: ", num_products)
        for _, entry in predicted_products.items():
            fp += entry['quantity']

        overall_num_preds += num_preds
        overall_products += num_products
        print("Detected products for {}: {}/{}, correct products {}/{}, correct association {}/{}".format(
            dbName, num_preds, num_products, num_correct_products, num_preds, num_correct_asso, num_correct_products))
    
    print("\n================== Evaluation Summary ==================")
    print("Databases: ", dbs)
    print("Ground truth version: ", gt_path)
    print("Overall products detection rate is: {:.1f}%".format(overall_num_preds*100.0 / overall_products))
    print("Overall association accuracy is: {:.1f}%".format(tp_asso*100.0/ tp))
    print("Overall precision is: {:.1f}%".format(tp*100.0 / (tp+fp)))
    print("Overall recall is: {:.1f}%".format(tp*100.0 / (tp+fn)))

if __name__ == "__main__":
    dbs=['cps-test-01', 'cps-test-2'] + ['cps-test-'+str(i) for i in range(4, 13)]
    gt_path='ground_truth/v10.json' # list of ground truth W.R.T the previous databases
    # dbs = ['cps-test-10', 'cps-test-11', 'cps-test-12']
    evaluate_intenvory(dbs, gt_path)