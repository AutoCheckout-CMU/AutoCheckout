import numpy as np
from pymongo import MongoClient
from collections import namedtuple
import cpsdriver.codec as codec
import GroundTruth as GT
import math


__mongoClient = MongoClient('localhost:27017')
db = __mongoClient['cps-test-01']
planogramDB = db['planogram']
productsDB = db['products']
plateDB = db['plate_data']

__frameDB = db['frame_message']
__planogram = None
__productsCache = {}
__relativePositionsPerProduct = {}
__absoluteCoordinatesPerProduct = {}

# store meta
__gondolasDict = None
__shelvesDict = None
__platesDict = None


def __loadPlanogram():
    num_gondola = 5
    num_shelf = 6
    num_plate = 12
    planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)

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

def getProductByID(productID):
    if productID in __productsCache:
        return __productsCache[productID]
    else:
        product = codec.Product.from_dict(productsDB.find_one({'product_id.id': productID}))
        __productsCache[productID] = product
        return product


def getFramesForEvent(event):
    timeBegin = event.triggerBegin
    timeEnd = event.triggerEnd
    frames = {}
    # TODO: date_time different format in test 2
    framesCursor = __frameDB.find({
        'date_time': {
            '$gte': timeBegin,
            '$lt': timeEnd
        }
    })

    for frameDoc in framesCursor:
        cameraID = frameDoc['camera_id']
        if cameraID not in frames:
            frames[cameraID] = frameDoc
        else:
            if frames[cameraID]['date_time'] > frameDoc['date_time']:
                # pick an earlier frame for this camera
                frames[cameraID] = frameDoc
    
    for frameKey in frames:
        rgbFrame = codec.DocObjectCodec.decode(frames[frameKey], 'frame_message')
        frames[frameKey] = rgbFrame

    print(len(frames))

def __findOptimalPlateForEvent(event):
    return 1

def __get3DCoordinatesForPlate(gondola, shelf, plate):
    if __gondolasDict == None:
        __buildDictsFromStoreMeta()
    gondolaMetaKey = str(gondola)
    shelfMetaKey = str(gondola) + '_' + str(shelf)
    plateMetaKey = str(gondola) + '_' + str(shelf) + '_' + str(plate)

    #TODO: rotation values for one special gondola
    absolute3D = AbsoluteCoord(0, 0, 0)
    gondolaTranslation = __getTranslation(__gondolasDict[gondolaMetaKey])
    absolute3D.translateBy(gondolaTranslation['x'], gondolaTranslation['y'], gondolaTranslation['z'])

    shelfTranslation = __getTranslation(__shelvesDict[shelfMetaKey])
    absolute3D.translateBy(shelfTranslation['x'], shelfTranslation['y'], shelfTranslation['z'])

    plateTranslation = __getTranslation(__platesDict[plateMetaKey])
    absolute3D.translateBy(plateTranslation['x'], plateTranslation['y'], plateTranslation['z'])

def __getTranslation(meta):
    return meta['coordinates']['transform']['translation']


def __buildDictsFromStoreMeta():
    for gondolaMeta in GT.gondolasMeta:
        __gondolasDict[str(gondolaMeta['id']['id'])] = gondolaMeta

    for shelfMeta in GT.shelvesMeta:
        IDs = shelfMeta['id']
        gondolaID = IDs['gondola_id']['id']
        shelfID = IDs['shelf_index']
        shelfMetaIndexKey = str(gondolaID) + '_' + str(shelfID)
        __shelvesDict[shelfMetaIndexKey] = shelfMetaIndexKey

    for plateMeta in GT.platesMeta:
        IDs = plateMeta['id']
        gondolaID = IDs['shelf_id']['gondola_id']['id']
        shelfID = IDs['shelf_id']['shelf_index']
        plateID = IDs['plate_index']
        plateMetaIndexKey = str(gondolaID) + '_' + str(shelfID) + '_' + str(plateID)
        __platesDict[plateMetaIndexKey] = plateMeta
    

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
    
    def translateBy(self, delta_x, delta_y, delta_z):
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

# class Frame:


__planogram = __loadPlanogram()

__products = __loadProducts()

