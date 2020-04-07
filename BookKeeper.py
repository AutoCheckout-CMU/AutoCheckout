import numpy as np
from pymongo import MongoClient
from collections import namedtuple
import math


__mongoClient = MongoClient('localhost:27017')
db = __mongoClient['cps-test-01']
__DBsTuple = namedtuple('DBs', 'planogramDB, productsDB, plateDB')
DBs = __DBsTuple(planogramDB=db['planogram'], productsDB=db['products'], plateDB=db['plate_data'])

__planogram = None
__products = None
__relativePositionsPerProduct = {}
__absoluteCoordinatesPerProduct = {}

def __loadPlanogram():
    num_gondola = 5
    num_shelf = 6
    num_plate = 12
    planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)
    planogramDB = DBs.planogramDB

    for item in planogramDB.find():
        for plate in item['plate_ids']:
            shelf = plate['shelf_id']
            gondola = shelf['gondola_id']
            gondolaID = gondola['id']
            shelfID = shelf['shelf_index']
            plateID = plate['plate_index']

            productID = item['planogram_product_id']['id']
            globalCoordinates = item['global_coordinates']['transform']['translation']
            if productID != '':
                planogram[gondolaID-1][shelfID-1][plateID-1] = productID
                if productID not in __relativePositionsPerProduct:
                    __relativePositionsPerProduct[productID]  = []
                __relativePositionsPerProduct[productID].append((gondolaID, shelfID, plateID))

                # TODO: gondola 5 has rotation
                __absoluteCoordinatesPerProduct[productID] = globalCoordinates
    
    return  planogram

def __loadProducts():
    return None

def getProductFromRelativePos(*argv):
    gondola = argv[0]
    if len(argv) == 2:
        shelf = argv[1]
        return __planogram[gondola][shelf]
    if len(argv) == 3:
        shelf = argv[1]
        plate = argv[2]
        return __planogram[gondola][shelf][plate]

def getProductRelativePos(productID):
    positions = __relativePositionsPerProduct[productID]
    if len(positions) <= 0:
        return None
    middleIndex = math.floor(len(positions) / 2)
    midPos = positions[middleIndex]
    return RelativePos(midPos[0], midPos[1], midPos[2])
        

def getProductAbsolutePos(productID):
    pos = __absoluteCoordinatesPerProduct[productID]
    return AbsoluteCoord(pos['x'], pos['y'], pos['z'])

class RelativePos:
    def __init__(self, gondola, shelf, plate):
        self.gondola = gondola
        self.shelf = shelf
        self.plate = plate

class AbsoluteCoord: 
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

__planogram = __loadPlanogram()

__products = __loadProducts()

