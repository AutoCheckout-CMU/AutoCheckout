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


class CustomerReceipt():
    """
    checkIn/Out: time when customer enters/leaves the store
    customerID: identify of each customer
    purchaneList: [PickUpEvent], containing all the purchased items
    """
    checkIn: datetime
    checkOut: datetime
    customerID: int
    purchaseList: list
    def __init__(self, customerID):
        self.customerID = customerID

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


receipts = []

for event in events:
    print('=======')
    print(event.triggerBegin)
    print('=======')
    print(event.triggerEnd)

    # BK.getFramesForEvent(event)

    # a trivial implementation
    # get all products on this shelf

    # TODO: omg this is weird. might need to concatenate adjacent events
    if event.deltaWeight > 0:
        continue
    
    plateIDs = event.plateIDs

    print(plateIDs)
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
                mostPossible = (product, totalProb)
    
    # print(mostPossible)
    receipts.append(mostPossible[0])


    # probWeight = computeWeightProbability(event['delta_weight'], weight_plate_mean, weight_plate_std)
print(receipts)
