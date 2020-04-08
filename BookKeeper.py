import numpy as np
from pymongo import MongoClient
from collections import namedtuple
import cpsdriver.codec as codec
import GroundTruth as GT
import math
from typing import NamedTuple


_mongoClient = MongoClient('localhost:27017')
db = _mongoClient['cps-test-2']
planogramDB = db['planogram']
productsDB = db['products']
plateDB = db['plate_data']

_frameDB = db['frame_message']
_planogram = None
_productsCache = {}
_positionsPerProduct = {}
_coordinatesPerProduct = {}

# store meta
_gondolasDict = None
_shelvesDict = None
_platesDict = None


def _loadPlanogram():
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
                if productID not in _positionsPerProduct:
                    _positionsPerProduct[productID]  = []
                _positionsPerProduct[productID].append((gondolaID, shelfID, plateID))

                # TODO: gondola 5 has rotation
                _coordinatesPerProduct[productID] = globalCoordinates
    
    return  planogram

def _loadProducts():
    return None


def getProductByID(productID):
    if productID in _productsCache:
        return _productsCache[productID]
    else:
        product = codec.Product.from_dict(productsDB.find_one({'product_id.id': productID}))

        productExtended = ProductExtended()
        productExtended.barcode_type = product.product_id.barcode_type
        productExtended.barcode = product.product_id.barcode
        productExtended.name = product.name
        productExtended.thumbnail = product.thumbnail
        productExtended.price = product.price
        productExtended.weight = product.price
        productExtended.positions = getProductPositions(productExtended.barcode)
        print(productExtended.positions)
        _productsCache[productID] = productExtended
        return productExtended

def getFramesForEvent(event):
    timeBegin = event.triggerBegin
    timeEnd = event.triggerEnd
    frames = {}
    # TODO: date_time different format in test 2
    framesCursor = _frameDB.find({
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

def _findOptimalPlateForEvent(event):
    return 1

def _get3DCoordinatesForPlate(gondola, shelf, plate):
    if _gondolasDict == None:
        _buildDictsFromStoreMeta()
    gondolaMetaKey = str(gondola)
    shelfMetaKey = str(gondola) + '_' + str(shelf)
    plateMetaKey = str(gondola) + '_' + str(shelf) + '_' + str(plate)

    #TODO: rotation values for one special gondola
    absolute3D = Coordinates(0, 0, 0)
    gondolaTranslation = _getTranslation(_gondolasDict[gondolaMetaKey])
    absolute3D.translateBy(gondolaTranslation['x'], gondolaTranslation['y'], gondolaTranslation['z'])

    shelfTranslation = _getTranslation(_shelvesDict[shelfMetaKey])
    absolute3D.translateBy(shelfTranslation['x'], shelfTranslation['y'], shelfTranslation['z'])

    plateTranslation = _getTranslation(_platesDict[plateMetaKey])
    absolute3D.translateBy(plateTranslation['x'], plateTranslation['y'], plateTranslation['z'])

def _getTranslation(meta):
    return meta['coordinates']['transform']['translation']


def _buildDictsFromStoreMeta():
    for gondolaMeta in GT.gondolasMeta:
        _gondolasDict[str(gondolaMeta['id']['id'])] = gondolaMeta

    for shelfMeta in GT.shelvesMeta:
        IDs = shelfMeta['id']
        gondolaID = IDs['gondola_id']['id']
        shelfID = IDs['shelf_index']
        shelfMetaIndexKey = str(gondolaID) + '_' + str(shelfID)
        _shelvesDict[shelfMetaIndexKey] = shelfMetaIndexKey

    for plateMeta in GT.platesMeta:
        IDs = plateMeta['id']
        gondolaID = IDs['shelf_id']['gondola_id']['id']
        shelfID = IDs['shelf_id']['shelf_index']
        plateID = IDs['plate_index']
        plateMetaIndexKey = str(gondolaID) + '_' + str(shelfID) + '_' + str(plateID)
        _platesDict[plateMetaIndexKey] = plateMeta
    

def getProductIDsFromPosition(*argv):
    gondolaIdx = argv[0] - 1
    if len(argv) == 2:
        shelfIdx = argv[1] - 1
        # remove Nones
        products = [product for product in _planogram[gondolaIdx][shelfIdx] if product]
        # deduplication
        products = list(dict.fromkeys(products))
        return products
    if len(argv) == 3:
        shelfIdx = argv[1] - 1
        plateIdx = argv[2] - 1
        return _planogram[gondolaIdx][shelfIdx][plateIdx]

def getProductPosAverage(productID):
    positions = _positionsPerProduct[productID]
    if len(positions) <= 0:
        return None
    middleIndex = math.floor(len(positions) / 2)
    midPos = positions[middleIndex]
    return Position(midPos[0], midPos[1], midPos[2])

def getProductPositions(productID):
    positions = []
    for pos in _positionsPerProduct[productID]:
        positions.append(Position(pos[0], pos[1], pos[2]))
    return positions

def getProductCoordinates(productID):
    coord = _coordinatesPerProduct[productID]
    return Coordinates(coord['x'], coord['y'], coord['z'])

class Position():
    gondola: int
    shelf: int
    plate: int
    def __init__(self, gondola, shelf, plate):
        self.gondola = gondola
        self.shelf = shelf
        self.plate = plate
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Position(gondola=%d, shelf=%d, plate=%d)' % (self.gondola, self.shelf, self.plate)

class Coordinates: 
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def translateBy(self, delta_x, delta_y, delta_z):
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

# class Frame:

class ProductExtended():
    barcode_type: str
    barcode: str
    name: str
    thumbnail: str
    price: float
    weight: float
    positions: list
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return 'Product(barcode_type=%s, barcode=%s, name=%s, thumbnail=%s, price=%f, weight=%f, positions=%s)' % (
            self.barcode_type,
            self.barcode,
            self.name,
            self.thumbnail,
            self.price,
            self.weight,
            str(self.positions)
        )
_planogram = _loadPlanogram()

_products = _loadProducts()

