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


        # weight_mean,weight_std,timestamps,date_times = weightTrigger.get_weights_per_shelf()

        # weight_plate_mean,weight_plate_std,weight_shelf_mean,weight_shelf_std,timestamps,date_times = weightTrigger.get_weights()
        weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std = weightTrigger.get_moving_weight()
        
        number_gondolas = 5
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
            # assert (timestamps_count == weight_shelf_mean[i].shape[1])
            # assert (timestamps_count == weight_shelf_std[i].shape[1])
            # assert (timestamps_count == weight_plate_mean[i].shape[2])
            # assert (timestamps_count == weight_plate_std[i].shape[2])
            
        events = weightTrigger.detect_weight_events(weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std, timestamps)

        # def computeWeightProbability(deltaW, weight_mean, weight_std, weightScaleVar=1):
        #     p = np.zeros((len(weight_mean), 1))
        #     for i in range(0, len(weight_mean)-1):
        #         p[i] = math_utils.areaUnderTwoGaussians(weight_mean[i], weight_std[i], abs(deltaW), weightScaleVar)
        #     return p


        # Non-associated purchasing products
        active_products = []

        # dictionary recording all receipts
        # KEY: customer ID, VALUE: CustomerReceipt
        receipts = {}
        print("Capture {} events in the databse {}".format(len(events), dbName))
        for event in events:
            if VERBOSE:
                print('=======')
                print (event)
                print('=======')

            scoreCalculator = ScoreCalculator(myBK, event)

            # a trivial implementation
            # get all products on this shelf

            # TODO: omg this is weird. might need to concatenate adjacent events
            isPutbackEvent = False
            if event.deltaWeight > 0:
                isPutbackEvent = True
            

            # ProductScore
            topProductScore = scoreCalculator.getTopK(1)[0]
            # for score in scoreCalculator.getTopK(5):
            #     print(score)
            topProductExtended = myBK.getProductByID(topProductScore.barcode)

            active_products.append((topProductExtended, topProductScore.getTotalScore()))

            ################################ Naive Association ################################
            product, _ = active_products[-1] 
            productID = product.barcode
            # absolutePos = myBK.getProductCoordinates(productID)
            absolutePos = event.getEventCoordinates(myBK)
            targets = myBK.getTargetsForEvent(event)

            # No target for the event found at all
            if (len(targets)==0):
                continue
            
            id_result, target_result =  associate_product_naive(absolutePos, targets)
            # print(id_result, target_result)

            # # Use the trigger end time to capture the frame
            # timestamp = event.triggerEnd.timestamp()
            # print("Trigger end time stamp is: ", timestamp)
            # frames = BK.getFramesForEvent(event)
            # print("Frame length: ", len(frames))
            # camera_id = 4
            # camera_frame = frames[camera_id]

            ################################ Update receipt records ################################
            # New customer, create a new receipt
            if id_result not in receipts:
                customer_receipt = CustomerReceipt(id_result)
                receipts[id_result] = customer_receipt
            # Existing customer, update receipt
            else:
                customer_receipt = receipts[id_result]
            
            # Predict quantity from delta weight
            pred_quantity = max(int(round(abs(event.deltaWeight / product.weight))), 1)
            print("Predicted Quantity for ",  product.name, " is: ", event.deltaWeight / product.weight, product.thumbnail)
            if isPutbackEvent:
                if DEBUG:
                    customer_receipt.purchase(product, pred_quantity) # In the evaluation code, putback is still an event, so we accumulate for debug purpose
                else:
                    customer_receipt.putback(product, pred_quantity)
            else:
                customer_receipt.purchase(product, pred_quantity)

            # probWeight = computeWeightProbability(event['delta_weight'], weight_plate_mean, weight_plate_std)

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
    
    def output_json(self, db_id, user, receipts, path):
        import json
        print ('=======================')
        output = {}
        output['testcase'] = db_id
        output['user'] = user
        receipts_json = []
        for id_result in receipts:
            receipt = receipts[id_result]
            receipt_json = {}
            receipt_json['target_id'] = id_result
            products = []
            for purchase in receipt.purchaseList:
                product = {}
                product['barcode'] = purchase
                product['quantity'] = 1
                products.append(product)
            receipt_json['receipts'] = products
            receipts_json.append(receipt_json)
        output['receipts'] = receipts_json
        with open('output.json', 'w') as outfile:
            json.dump(output, outfile)


# myCashier = Cashier()
# db_name = 'cps-test-01'
# #db_name = 'TEAM-PEI-JD-1'
# db_id = '5aa089fd-1c62-46ce-8c02-3cc24f05e5ac'
# receipts = myCashier.process(db_name)
# user = '5ea023be-b530-4816-8eda-5340cfabe9b0'
# myCashier.output_json(db_id, user, receipts, path="output.json")

