from pymongo import MongoClient
import numpy as np
import base64
# from cpsdriver.codec import DocObjectCodec
import cpsdriver.codec as codec
import datetime as dt
from datetime import datetime
from WeightTrigger import WeightTrigger as WT
import BookKeeper as BK
import math_utils
import math
from ScoreCalculate import *

from utils import *
from config import *

# 0.75 might be better but its results jitter betweeen either 82.4 or 83.2???
PUTBACK_JITTER_RATE = 0.75
GRAB_FROM_SHELF_JITTER_RATE = 0.1

class CustomerReceipt():
    """
    checkIn/Out (datetime): time when customer enters/leaves the store
    customerID (String): identify of each customer
    purchaseList (Dict):
        KEY: product ID
        Value: (product, quantities)
    target (BK.Target): Target object for this customer
    """
    def __init__(self, customerID):
        self.customerID = customerID
        # productID -> (product, num_product)
        self.purchaseList = {} 

    def purchase(self, product, num_product):
        productID = product.barcode
        if productID in self.purchaseList:
            product, quantity = self.purchaseList[productID]
            self.purchaseList[productID] = (product, quantity+num_product)
        else:
            self.purchaseList[productID] = (product, num_product)

    def putback(self, product, num_product):
        productID = product.barcode
        if productID in self.purchaseList:
            product, quantity = self.purchaseList[productID]
            if quantity > num_product:
                self.purchaseList[productID] = (product, quantity-num_product)
            else:
                del self.purchaseList[productID]

"""
Cashier class to generate receipts
"""
class Cashier():
    def __init__(self):
        pass
    
    def process(self, dbName):
        myBK = BK.BookKeeper(dbName)
        weightTrigger = WT(myBK)

        # weight_plate_mean,weight_plate_std,weight_shelf_mean,weight_shelf_std,timestamps,date_times = weightTrigger.get_weights()
        weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std = weightTrigger.get_moving_weight()
        
        
        number_gondolas = len(weight_shelf_mean)
        # reduce timestamp 
        timestamps = weightTrigger.get_agg_timestamps()
        for i in range(number_gondolas):
            timestamps[i] = timestamps[i][30:-29]

        # sanity check
        for i in range(number_gondolas):
            # weight_shelf_mean: [gondola, shelf, timestamp]
            # weight_shelf_std: [gondola, shelf, timestamp]
            # weight_plate_mean: [gondola, shelf, plate, timestamp]
            # weight_plate_std: [gondola, shelf, plate, timestamp]
            # timestamps: [gondola, timestamp]
            timestamps_count = len(timestamps[i])
            # print ('weight_shelf_mean', weight_shelf_mean[i].shape)
            # print ('weight_shelf_std',  weight_shelf_std[i].shape)
            # print ('weight_plate_mean', weight_plate_mean[i].shape)
            # print ('weight_plate_std', weight_plate_std[i].shape)
            # print ('timestamps', timestamps_count)
            assert (timestamps_count == weight_shelf_mean[i].shape[1])
            assert (timestamps_count == weight_shelf_std[i].shape[1])
            assert (timestamps_count == weight_plate_mean[i].shape[2])
            assert (timestamps_count == weight_plate_std[i].shape[2])
            # print ('timestamps', timestamps[i][0], "to", timestamps[i][-1])
            
        events = weightTrigger.detect_weight_events(weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std, timestamps)
        events = weightTrigger.splitEvents(events)
        events.sort(key=lambda pickUpEvent:pickUpEvent.triggerBegin)
        # Non-associated purchasing products
        active_products = []

        # dictionary recording all receipts
        # KEY: customer ID, VALUE: CustomerReceipt
        receipts = {}
        print("Capture {} events in the databse {}".format(len(events), dbName))
        print("==============================================================")
        for event in events:
            if VERBOSE:
                print ("----------------")
                print ('Event: ', event)

            ################################ Naive Association ################################
            
            # absolutePos = myBK.getProductCoordinates(productID)
            absolutePos = event.getEventCoordinates(myBK)
            targets = myBK.getTargetsForEvent(event)
            # Initliaze a customer receipt for all new targets
            for target_id in targets.keys():
                if target_id not in receipts:
                    customer_receipt = CustomerReceipt(target_id)
                    receipts[target_id] = customer_receipt

            # No target for the event found at all
            if (len(targets)==0):
                continue
            
            if ASSOCIATION_TYPE == CE_ASSOCIATION:
                target_id, _ =  associate_product_ce(absolutePos, targets)
            elif ASSOCIATION_TYPE == CLOSEST_ASSOCIATION:
                target_id, _ = associate_product_closest(absolutePos, targets)
            else:
                target_id, _ =  associate_product_naive(absolutePos, targets)


             ################################ Calculate score ################################

            # TODO: omg this is weird. might need to concatenate adjacent events
            isPutbackEvent = False
            if event.deltaWeight > 0:
                isPutbackEvent = True
                # get all products pickedup by this target
                if target_id not in receipts:
                    continue
                customer_receipt = receipts[target_id]
                purchase_list = customer_receipt.purchaseList #  productID -> (product, num_product)

                # find most possible putback product whose weight is closest to the event weight
                candidate_products = []
                for item in purchase_list.values():
                    product, num_product = item
                    for count in range(1, num_product+1):
                        candidate_products.append((product, count))
                
                if (len(candidate_products) == 0):
                    continue
                # item = (product, count)
                candidate_products.sort(key=lambda item:abs(item[0].weight*item[1] - event.deltaWeight))
                product, putback_count = candidate_products[0]
                
                # If weight difference is too large, ignore this event
                if (abs(event.deltaWeight) < PUTBACK_JITTER_RATE*product.weight):
                    continue

                # Put the product on the shelf will affect planogram
                myBK.addProduct(event.getEventAllPositions(myBK), product)
            else:    
                scoreCalculator = ScoreCalculator(myBK, event)
                topProductScore = scoreCalculator.getTopK(1)[0]
                if VERBOSE:
                    print ("top 5 predicted products:")
                    for productScore in  scoreCalculator.getTopK(5):
                        print(productScore)

                topProductExtended = myBK.getProductByID(topProductScore.barcode)

                product = topProductExtended

                # If weight difference is too large, ignore this event
                if (abs(event.deltaWeight) < GRAB_FROM_SHELF_JITTER_RATE*product.weight):
                    continue
            productID = product.barcode

            ################################ Update receipt records ################################
            # New customer, create a new receipt
            if target_id not in receipts:
                customer_receipt = CustomerReceipt(target_id)
                receipts[target_id] = customer_receipt
            # Existing customer, update receipt
            else:
                customer_receipt = receipts[target_id]
            
            if isPutbackEvent:
                # Putback count from previous step
                pred_quantity = putback_count
                if DEBUG:
                    customer_receipt.purchase(product, pred_quantity) # In the evaluation code, putback is still an event, so we accumulate for debug purpose
                else:
                    customer_receipt.putback(product, pred_quantity)
            else:
                # Predict quantity from delta weight
                pred_quantity = max(int(round(abs(event.deltaWeight / product.weight))), 1)
                customer_receipt.purchase(product, pred_quantity)

            if VERBOSE:
                print("Predicted: [%s][putback=%d] %s, weight=%dg, count=%d, thumbnail=%s" % (product.barcode, isPutbackEvent, product.name, product.weight, pred_quantity, product.thumbnail))
            else:
                print("Predicted: [%s][putback=%d] %s, weight=%dg, count=%d" % (product.barcode, isPutbackEvent, product.name, product.weight, pred_quantity))


        ################ Display all receipts ################
        if VERBOSE:
            num_receipt = 0
            if (len(receipts) == 0):
                print("No receipts!")
                return {}
        
            for id, customer_receipt in receipts.items():
                print("============== Receipt {} ==============".format(num_receipt))
                print("Customer ID: " + id)
                print("Purchase List: ")
                for _, entry in customer_receipt.purchaseList.items():
                    product, quantity = entry
                    print("*Name: "+product.name + ", Quantities: " + str(quantity), product.thumbnail)
                num_receipt += 1
        
        return receipts
