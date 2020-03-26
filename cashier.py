from pymongo import MongoClient
import numpy as np
import base64
from cpsdriver.codec import DocObjectCodec
import datetime as dt
from WeightTrigger import WeightTrigger
import math_utils
import math

mongoClient = MongoClient('localhost:27017')

db = mongoClient['cps-test-01']

weightTrigger = WeightTrigger(db)
# print(weightTrigger.plate_data)



# weight_mean,weight_std,timestamps,date_times = weightTrigger.get_weights_per_shelf()

weight_plate_mean,weight_plate_std,weight_shelf_mean,weight_shelf_std,timestamps,date_times = weightTrigger.get_weights()

print(len(weight_plate_mean))


events = weightTrigger.detect_weight_events(weight_shelf_mean, weight_shelf_std, weight_plate_mean, weight_plate_std, date_times)

# print(len(events))


def loadPlanogram():

    num_gondola = 5
    num_shelf = 6
    num_plate = 12
    planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)
    planogramDB = db['planogram']


    for item in planogramDB.find():
        for plate in item['plate_ids']:
            shelf = plate['shelf_id']
            gondola = shelf['gondola_id']
            gondolaID = gondola['id']
            shelfID = shelf['shelf_index']
            plateID = plate['plate_index']

            planogram[gondolaID-1][shelfID-1][plateID-1] = item['planogram_product_id']['id']

    return planogram


def computeWeightProbability(deltaW, weight_mean, weight_std, weightScaleVar=1):
    p = np.zeros((len(weight_mean), 1))
    for i in range(0, len(weight_mean)-1):
        p[i] = math_utils.areaUnderTwoGaussians(weight_mean[i], weight_std[i], abs(deltaW), weightScaleVar)
    return p

planogram = loadPlanogram()

receipts = []

for event in events:

    # event = {'trigger_begin': trigger_begin,
    #         'trigger_end': trigger_end,
    #         'n_begin': n_begin,
    #         'n_end': n_end,
    #         'delta_weight': delta_w,
    #         'gondola': gondola_id + 1,
    #         'shelf': shelf_id + 1,
    #         'plates': plates, 
    #         }

    # a trivial implementation
    # get all products on this shelf

    # TODO: omg this is weird. might need to concatenate adjacent events
    if event['delta_weight'] > 0:
        continue

    gondolaIndex = event['gondola'] - 1
    shelfIndex = event['shelf'] - 1
    plates = event['plates']
    print(plates)
    # a trivial mean plate number

   

    possibleProductIDs = planogram[gondolaIndex][shelfIndex]
    # print(possibleProductIDs)

    productsDB = db['products']
    products = {}

    arrangementProbabilityPerProduct = {}
    weightProbabilityPerProduct = {}

    totalProbabilityPerProduct = {}
    
    for productID in possibleProductIDs:
        if (productID in arrangementProbabilityPerProduct) != True:
            products[productID] = productsDB.find_one({'product_id.id': productID})

            arrangementProbabilityPerProduct[productID] = 0
            weightProbabilityPerProduct[productID] = 0
            totalProbabilityPerProduct[productID] = 0

            

    # arrangement probability
    plateProb = 0
    probPerPlate = []
    if (sum(plates) == 0):
        plateProb = 1/len(plates)
        for i in range(0, len(plates)):
            probPerPlate.append(plateProb)
    else:
        plateProb = 1/sum(plates)
        for plate in plates:
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
        weight = product['metadata']['weight']

        # When productW=deltaW, e^(-|productW - deltaW|)=1.0
        
        weightProb = (math.e)**(-abs(weight-abs(event['delta_weight'])))
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