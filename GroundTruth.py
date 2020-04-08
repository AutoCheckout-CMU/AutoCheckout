import json
from collections import namedtuple
from pymongo import MongoClient
import BookKeeper

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.load(data, object_hook=_json_object_hook)

groundTruth = None

with open('ground_truth/v3.json', 'r') as f:
    groundTruth = json2obj(f)


products = {}

class GTLabeler:
    def __init__(self):
        gt = GroundTruth()
        for dataset in groundTruth.lists:
            objEvents = []
            for event in dataset.events:
                isProductIncluded = {}
                productList = []
                position = event.observation.position

                for plate in position.plates:
                    productID = BookKeeper.getProductIDsFromPosition(position.gondola, position.shelf, position.plate)
                    if (productID in isProductIncluded) != True:
                        isProductIncluded[productID] = True
                        if (productID in products) != True:
                            product = BookKeeper.getProductByID(productID)
                            if product == None:
                                continue
                                print(product['product_id']['id'])
                            objProduct = Product(
                                product['product_id']['id'],
                                product['product_id']['barcode_type'],
                                product['metadata']['name'],
                                product['metadata']['thumbnail'],
                                product['metadata']['price'],
                                product['metadata']['weight']
                            )
                            # print(objProduct.toJSON())
                            products[productID] = objProduct
                        productList.append(products[productID])
                objPosition = PositionGT(position.gondola, position.shelf, position.plates)
                objObservation = ObservationGT(productList, event.observation.time, objPosition, getattr(event.observation, 'todo', None))
                objEvent = EventGT(event.eventID, event.putback, objObservation)
                objEvents.append(objEvent)
            objDataset = DatasetGT(dataset.dataset, objEvents)
            gt.lists.append(objDataset)
        
        print(len(gt.lists))
        dump = open("ground_truth/v6.json", 'w')
        dump.write(gt.toJSON())

class Serializable:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=2)

class GroundTruth(Serializable):
    def __init__(self):
        self.lists = []

class PositionGT(Serializable):
    def __init__(self, gondola, shelf, plates):
        self.gondola = gondola
        self.shelf = shelf
        self.plates = plates

class ProductGT(Serializable):
    def __init__(self, id, barcodeType, name, thumbnail, price, weight):
        self.id = id
        self.barcodeType = barcodeType
        self.name = name
        self.thumbnail = thumbnail
        self.price = price
        self.weight = weight

class ObservationGT(Serializable):
    def __init__(self, products, time, position, todo):
        self.products = products
        self.time = time
        self.position = position
        self.todo = todo

class EventGT(Serializable):
    def __init__(self, eventID, putback, observation):
        self.eventID = eventID
        self.putback = putback
        self.observation = observation

class DatasetGT(Serializable):
    def __init__(self, dataset, events):
        self.dataset = dataset
        self.events = events

# gondolasMeta = None
# shelvesMeta = None
# platesMeta = None
with open('./store_meta/Gondolas.json') as f:
    gondolasMeta = json.load(f)['gondolas']
with open('./store_meta/Shelves.json') as f:
    shelvesMeta = json.load(f)['shelves']
with open('./store_meta/Plates.json') as f:
    platesMeta = json.load(f)['plates']

print(len(gondolasMeta))
print(len(shelvesMeta))
print(len(platesMeta))

# {
#   "lists": [
#     {
#       "dataset": "2019-11-07_02-35",
#       "events": [
#         {
#           "eventID": 1,
#           "putback": 0,
#           "observe": {
#             "product": "",
#             "time": "2019-11-07_02-35-28",
#             "position": {
#               "gondola": 2,
#               "shelf": 6,
#               "plates": [
#                 8,
#                 9
#               ]
#             }
#           }
#         },
#         {
#           "eventID": 1,
#           "putback": 0,
#           "observe": {
#             "product": "",
#             "time": "2019-11-07_02-35-28",
#             "position": {
#               "gondola": 2,
#               "shelf": 6,
#               "plates": [
#                 8,
#                 9
#               ]
#             }
#           }
#         }
#       ]
#     }
#   ]
# }

# class GroundTruth(Serializable):

# if __name__ == '__main__':
#     """Main function"""
#     gtLabeler = GTLabeler()
