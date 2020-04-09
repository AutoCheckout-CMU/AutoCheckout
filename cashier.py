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


class CustomerReceipt():
    """
    checkIn/Out (datetime): time when customer enters/leaves the store
    customerID (String): identify of each customer
    purchaseList (list): [PickUpEvent], containing all the purchased items
    target (BK.Target): Target object for this customer
    """
    def __init__(self, customerID):
        self.customerID = customerID
        self.purchaseList = []

    def purchase(self, product):
        self.purchaseList.append(product)


weightTrigger = WT()


# weight_mean,weight_std,timestamps,date_times = weightTrigger.get_weights_per_shelf()

# weight_plate_mean,weight_plate_std,weight_shelf_mean,weight_shelf_std,timestamps,date_times = weightTrigger.get_weights()
weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std = weightTrigger.get_moving_weight()
date_times = weightTrigger.get_agg_date_times()


events = weightTrigger.detect_weight_events(weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std, date_times)

# print(len(events))



def computeWeightProbability(deltaW, weight_mean, weight_std, weightScaleVar=1):
    p = np.zeros((len(weight_mean), 1))
    for i in range(0, len(weight_mean)-1):
        p[i] = math_utils.areaUnderTwoGaussians(weight_mean[i], weight_std[i], abs(deltaW), weightScaleVar)
    return p


# Non-associated purchasing products
active_products = []

# dictionary recording all receipts
# KEY: customer ID, VALUE: CustomerReceipt
receipts = {}

for event in events:
    print('=======')
    print(event.triggerBegin)
    print('=======')
    print(event.triggerEnd)

    # a trivial implementation
    # get all products on this shelf

    # TODO: omg this is weird. might need to concatenate adjacent events
    if event.deltaWeight > 0:
        continue
    
    plateIDs = event.plateIDs

    # print(plateIDs)
    # a trivial mean plate number
    possibleProductIDs = BK.getProductIDsFromPosition(event.gondolaID, event.shelfID)
    # print(possibleProductIDs)

    products = {}

    arrangementProbabilityPerProduct = {}
    weightProbabilityPerProduct = {}

    totalProbabilityPerProduct = {}
    
    for productID in possibleProductIDs:
        if productID not in arrangementProbabilityPerProduct:
            products[productID] = BK.getProductByID(productID)

            arrangementProbabilityPerProduct[productID] = 0
            weightProbabilityPerProduct[productID] = 0
            totalProbabilityPerProduct[productID] = 0

            

    # arrangement probability
    plateProb = 0
    probPerPlate = []
    if (sum(plateIDs) == 0):
        plateProb = 1/len(plateIDs)
        for i in range(0, len(plateIDs)):
            probPerPlate.append(plateProb)
    else:
        plateProb = 1/sum(plateIDs)
        for plate in plateIDs:
            if plate == 0:
                probPerPlate.append(0)
            else:
                probPerPlate.append(plateProb)
    
    for i in range(0, len(possibleProductIDs)):
        productID = possibleProductIDs[i]
        arrangementProbabilityPerProduct[productID] += probPerPlate[i]

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
                mostPossible = (product, totalProb, event.triggerEnd)

    active_products.append(mostPossible)

    ################################ Naive Association ################################
    product, _, _ = active_products[-1]
    productID = product.barcode
    absolutePos = BK.getProductCoordinates(productID)
    
    targets = BK.getTargetsForEvent(event)
    
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
    
    customer_receipt.purchase(product)

    # probWeight = computeWeightProbability(event['delta_weight'], weight_plate_mean, weight_plate_std)

print("\n")
################ Display all receipts ################
num_receipt = 0
for id, customer_receipt in receipts.items():
    print("============== Receipt {} ==============".format(num_receipt))
    print("Customer ID: " + id)
    print("Purchase List: ")
    for product in customer_receipt.purchaseList:
        print("*"+product.name)