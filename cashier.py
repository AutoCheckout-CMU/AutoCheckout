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

    def purchase(self, product):
        productID = product.barcode
        if productID in self.purchaseList:
            product, quantity = self.purchaseList[productID]
            self.purchaseList[productID] = (product, quantity+1)
        else:
            self.purchaseList[productID] = (product, 1)

    def putback(self, product):
        productID = product.barcode
        if productID in self.purchaseList:
            product, quantity = self.purchaseList[productID]
            if quantity > 1:
                self.purchaseList[productID] = (product, quantity-1)
            else:
                del self.purchaseList[productID]

"""
Cashier class to generate receipts
"""
class Cashier():
    def __init__(self):
        pass
    
    def process(self, dbName='cps-test-01'):
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
            assert (timestamps_count == weight_shelf_mean[i].shape[1])
            assert (timestamps_count == weight_shelf_std[i].shape[1])
            assert (timestamps_count == weight_plate_mean[i].shape[2])
            assert (timestamps_count == weight_plate_std[i].shape[2])
            
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

            # a trivial implementation
            # get all products on this shelf

            # TODO: omg this is weird. might need to concatenate adjacent events
            isPutbackEvent = False
            if event.deltaWeight > 0:
                isPutbackEvent = True
            
            plateIDs = event.plateIDs

            # print(plateIDs)
            # a trivial mean plate number
            possibleProductIDs = myBK.getProductIDsFromPosition(event.gondolaID, event.shelfID)
            # print(possibleProductIDs)

            products = {}

            arrangementProbabilityPerProduct = {}
            weightProbabilityPerProduct = {}

            totalProbabilityPerProduct = {}
            
            for productID in possibleProductIDs:
                if productID not in arrangementProbabilityPerProduct:
                    products[productID] = myBK.getProductByID(productID)

                    arrangementProbabilityPerProduct[productID] = 0
                    weightProbabilityPerProduct[productID] = 0
                    totalProbabilityPerProduct[productID] = 0

                    

            # arrangement probability (with different weight sensed on different plate)
            plateProb = 0
            probPerPlate = []
            overallDelta = sum(plateIDs)
            # a potential bug: what if there are both negatives and positives and their sum is zero?
            if (overallDelta == 0):
                plateProb = 1/len(plateIDs)
                for i in range(0, len(plateIDs)):
                    probPerPlate.append(plateProb)
            else:
                # plateProb = 1/sum(plateIDs)
                # for plate in plateIDs:
                #     if plate == 0:
                #         probPerPlate.append(0)
                #     else:
                #         probPerPlate.append(plateProb)

                for plate in plateIDs:
                    probPerPlate.append(plate/overallDelta)
            for i in range(0, len(possibleProductIDs)):
                productID = possibleProductIDs[i]
                positions = myBK.getProductPositions(productID)
                for position in positions:
                    arrangementProbabilityPerProduct[productID] += probPerPlate[position.plate-1]

            # print(arrangementProbabilityPerProduct)

            # weight probability & total & find the most possible
            mostPossible = ()
            mostPossibleIsInitialized = False

            for productID in products:
                product = products[productID]
                weight = product.weight

                # When productW=deltaW, e^(-|productW - deltaW|)=1.0
                
                weightProb = (math.e)**(-abs(weight-abs(event.deltaWeight)))
                # print("======weight")
                # print(weightProb)
                weightProbabilityPerProduct[productID] = weightProb
                totalProb = weightProb + arrangementProbabilityPerProduct[productID]
                # print("======total")
                # print(totalProb)
                totalProbabilityPerProduct[productID] = totalProb
                if mostPossibleIsInitialized == False:
                    mostPossible = (product, totalProb)
                    mostPossibleIsInitialized = True
                else:
                    if mostPossible[1] <= totalProb:
                        mostPossible = (product, totalProb)
            
            active_products.append(mostPossible)

            ################################ Naive Association ################################
            product, _ = active_products[-1] 
            productID = product.barcode
            absolutePos = myBK.getProductCoordinates(productID)
            
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
            
            if isPutbackEvent:
                if DEBUG:
                    customer_receipt.purchase(product) # In the evaluation code, putback is still an event, so we accumulate for debug purpose
                else:
                    customer_receipt.putback(product)
            else:
                customer_receipt.purchase(product)

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
                    print("*Name: "+product.name + ", Quantities: " + str(quantity))
                num_receipt += 1
        return receipts

# myCashier = Cashier()
# myCashier.process('cps-test-2')
