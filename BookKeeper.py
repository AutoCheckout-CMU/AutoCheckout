import numpy as np
from pymongo import MongoClient
from collections import namedtuple
import cpsdriver.codec as codec
import GroundTruth as GT
import math
from typing import NamedTuple
import io
from PIL import Image, ImageDraw
from config import *
import json
import os
from datetime import datetime

INCH_TO_METER = 0.0254

class BookKeeper():
    def __init__(self, dbname):
        _mongoClient = MongoClient('mongodb://localhost:27017')
        self.__dbname = dbname
        self.db = _mongoClient[dbname]
        self.planogramDB = self.db['planogram']
        self.productsDB = self.db['products']
        self.plateDB = self.db['plate_data']
        self._targetsDB = self.db['full_targets']
        if self._targetsDB.count() == 0:
            self._targetsDB = self.db['targets']
        self._frameDB = self.db['frame_message']

        self._planogram = None
        self._productsCache = {}

        # store meta
        self._gondolasDict = {}
        self._shelvesDict = {}
        self._platesDict = {}
        
        self.productIDsFromPlanogramTable = set()
        self.productIDsFromProductsTable = set()

        self.__buildAllProductsCache()
        self. _planogram = self.__loadPlanogram()
        
        
        self._buildDictsFromStoreMeta()
        

    def __loadPlanogram(self):
        num_gondola = 5
        num_shelf = 6
        num_plate = 12
        planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)

        for item in self.planogramDB.find():
            
            if 'id' not in item['planogram_product_id']:
                continue
            productID = item['planogram_product_id']['id']
            if productID == '':
                continue
            productItem = self.productsDB.find_one({
                'product_id.id': productID,
            })
            product = codec.Product.from_dict(productItem)
            if product.weight == 0.0:
                continue
            
            productExtended = self.getProductByID(productID)
            for plate in item['plate_ids']:
                shelf = plate['shelf_id']
                gondola = shelf['gondola_id']
                gondolaID = gondola['id']
                shelfID = shelf['shelf_index']
                plateID = plate['plate_index']
                
                if planogram[gondolaID-1][shelfID-1][plateID-1] is None:
                    planogram[gondolaID-1][shelfID-1][plateID-1] = set()
                planogram[gondolaID-1][shelfID-1][plateID-1].add(productID)
                self.productIDsFromPlanogramTable.add(productID)

                productExtended.positions.add(Position(gondolaID, shelfID, plateID))
        
        return planogram

    def addProduct(self, positions, productExtended):
        for position in positions:
            gondolaID, shelfID, plateID = position.gondola, position.shelf, position.plate
            self._planogram[gondolaID-1][shelfID-1][plateID-1].add(productExtended.barcode)
            # Update product position
            if position not in productExtended.positions:
                productExtended.positions.add(position)

    def __buildAllProductsCache(self):
        for item in self.productsDB.find():
            product = codec.Product.from_dict(item)
            if product.weight == 0.0:
                continue

            productExtended = ProductExtended()
            productExtended.barcode_type = product.product_id.barcode_type
            productExtended.barcode = product.product_id.barcode
            productExtended.name = product.name
            productExtended.thumbnail = product.thumbnail
            productExtended.price = product.price
            productExtended.weight = product.weight
            productExtended.positions = set()

            # Workaround for database error: [JD] Good catch, the real weight is 538g, 
            # Our store operator made a mistake when inputing the product in :scales:
            if productExtended.barcode == '898999010007':
                productExtended.weight = 538.0
            
            # Workaround for database error: [JD] 1064g for the large one (ACQUA PANNA PET MINERAL DRINK), 800g for the small one
            if productExtended.barcode == '041508922487':
                productExtended.weight = 1064.0

            self._productsCache[productExtended.barcode] = productExtended
            self.productIDsFromProductsTable.add(productExtended.barcode)

    def getProductByID(self, productID):
        if productID in self._productsCache:
            return self._productsCache[productID]
        return None

    def getFramesForEvent(self, event):
        timeBegin = event.triggerBegin
        timeEnd = event.triggerEnd
        frames = {}
        # TODO: date_time different format in test 2
        framesCursor = self._frameDB.find({
            'timestamp': {
                '$gte': timeBegin,
                '$lt': timeEnd
            }
        })

        for frameDoc in framesCursor:
            cameraID = frameDoc['camera_id']
            if cameraID not in frames:
                frames[cameraID] = frameDoc
            else:
                if frames[cameraID]['date_time'] <= frameDoc['date_time']:
                    # pick an earlier frame for this camera
                    frames[cameraID] = frameDoc
        
        for frameKey in frames:
            # print("Frame Key (camera ID) is: ", frameKey)
            rgbFrame = codec.DocObjectCodec.decode(frames[frameKey], 'frame_message')
            imageStream = io.BytesIO(rgbFrame.frame)
            im = Image.open(imageStream)
            frames[frameKey] = im
        if VERBOSE:
            print("Capture {} camera frames in this event".format(len(frames)))
        return frames

    """
    Function to get a frame Image from the database
    Input:
        timestamp: double/string
        camera_id: int/string, if camera id is not specified, returns all the image with camera IDs
    Output:
        (with camera ID) PIL Image: Image object RGB format
        (without camera ID): dictionary {camera_id: PIL Image}
    """
    def getFrameImage(self, timestamp, camera_id=None):
        if camera_id is not None:
            framesCursor = self._frameDB.find({
                'timestamp': float(timestamp),
                'camera_id': int(camera_id)
            })
            # One timestamp should corresponds to only one frame
            if (framesCursor.count() == 0):
                return None
            item = framesCursor[0]
            rgb = codec.DocObjectCodec.decode(doc=item, collection='frame_message')
            imageStream = io.BytesIO(rgb.frame)
            im = Image.open(imageStream)
            return im
        else:
            image_dict = {}
            framesCursor = self._frameDB.find({
                'timestamp': float(timestamp),
            })
            if (framesCursor.count() == 0):
                return None
            for item in framesCursor:
                # print("Found image with camera id: ", item['camera_id'])
                camera_id = item['camera_id']
                rgb = codec.DocObjectCodec.decode(doc=item, collection='frame_message')
                imageStream = io.BytesIO(rgb.frame)
                im = Image.open(imageStream)
                image_dict[camera_id] = im
            return image_dict

    """
    Function to get lastest targets for an event
    Input:
        event
    Output:
        List[target]: all the in-store target during this event period
    """
    def getTargetsForEvent(self, event):
        timeBegin = event.triggerBegin
        timeEnd = event.triggerEnd
        targetsCursor = self._targetsDB.find({
            'timestamp': {
                '$gte': timeBegin,
                '$lt': timeEnd
            }
        })
        # print("Duration: ", timeBegin, timeEnd)
        # Sort the all targets entry in a timely order
        targetsCursor.sort([('timestamp', 1)])
        targets = {}
        num_timestamps = targetsCursor.count()
        for i, targetDoc in enumerate(targetsCursor):
            if 'targets' not in targetDoc['document']['targets']:
                continue
            target_list = targetDoc['document']['targets']['targets']
            for target in target_list:
                target_id = target['target_id']['id']
                valid_entrance = target['target_state'] == 'TARGETSTATE_VALID_ENTRANCE'
                # Head
                head = None
                if 'head' in target:
                    if (len(target['head']['point']) != 0):
                        x, y, z = target['head']['point']['x'], target['head']['point']['y'], target['head']['point']['z']
                        score = target['head']['score']
                        coordinate = Coordinates(x*INCH_TO_METER, y*INCH_TO_METER, z*INCH_TO_METER)
                        head = {'position': coordinate, 'score': score}
                left_hand, right_hand = None, None
                if CE_ASSOCIATION and 'l_wrist' in target and 'r_wrist' in target:
                    # Left hand
                    if (len(target['l_wrist']['point']) != 0):
                        lh_x, lh_y, lh_z = target['l_wrist']['point']['x'], target['l_wrist']['point']['y'], target['l_wrist']['point']['z']
                        lh_score = target['l_wrist']['score']
                        lh_coordinate = Coordinates(lh_x*INCH_TO_METER, lh_y*INCH_TO_METER, lh_z*INCH_TO_METER)
                        left_hand = {'position': lh_coordinate, 'score': lh_score}
                    else:
                        left_hand = None
                    # Right
                    if (len(target['r_wrist']['point']) != 0):
                        rh_x, rh_y, rh_z = target['r_wrist']['point']['x'], target['r_wrist']['point']['y'], target['r_wrist']['point']['z']
                        rh_score = target['r_wrist']['score']
                        rh_coordinate = Coordinates(rh_x*INCH_TO_METER, rh_y*INCH_TO_METER, rh_z*INCH_TO_METER)
                        right_hand = {'position': rh_coordinate, 'score': rh_score}
                    else:
                        right_hand = None

                if target_id not in targets:
                    # Create new target during this period
                    targets[target_id] = Target(target_id, head, left_hand, right_hand, valid_entrance)
                else:
                    # Update existing target
                    targets[target_id].update(target_id, head, left_hand, right_hand, valid_entrance)
            # print(i, num_timestamps, targetDoc['timestamp'])
            # print(targets.items())
            if (i>num_timestamps/2):
                # print("Trigger duration ", datetime.fromtimestamp(timeBegin), datetime.fromtimestamp(timeEnd))
                # print("Break at date time: ", targetDoc['date_time'])
                break
        # print("Event timestamp: ", targetDoc['timestamp'], head)
        if VERBOSE:
            print("Targets: Capture {} targets in this event".format(len(targets)), targets.keys())
        return targets

    def _findOptimalPlateForEvent(self, event):
        return 1

    def get3DCoordinatesForPlate(self, gondola, shelf, plate):
        gondolaMetaKey = str(gondola)
        shelfMetaKey = str(gondola) + '_' + str(shelf)
        plateMetaKey = str(gondola) + '_' + str(shelf) + '_' + str(plate)

        #TODO: rotation values for one special gondola
        absolute3D = Coordinates(0, 0, 0)
        gondolaTranslation = self._getTranslation(self._gondolasDict[gondolaMetaKey])
        absolute3D.translateBy(gondolaTranslation['x'], gondolaTranslation['y'], gondolaTranslation['z'])

        if gondola == 5:
            # rotate by 90 degrees
            shelfTranslation = self._getTranslation(self._shelvesDict[shelfMetaKey])
            absolute3D.translateBy(-shelfTranslation['y'], shelfTranslation['x'], shelfTranslation['z'])

            plateTranslation = self._getTranslation(self._platesDict[plateMetaKey])
            absolute3D.translateBy(-plateTranslation['y'], plateTranslation['x'], plateTranslation['z'])

        else:
            shelfTranslation = self._getTranslation(self._shelvesDict[shelfMetaKey])
            absolute3D.translateBy(shelfTranslation['x'], shelfTranslation['y'], shelfTranslation['z'])

            plateTranslation = self._getTranslation(self._platesDict[plateMetaKey])
            absolute3D.translateBy(plateTranslation['x'], plateTranslation['y'], plateTranslation['z'])
        
        
            
        return absolute3D

    def _getTranslation(self, meta):
        return meta['coordinates']['transform']['translation']


    def _buildDictsFromStoreMeta(self):
        for gondolaMeta in GT.gondolasMeta:
            self._gondolasDict[str(gondolaMeta['id']['id'])] = gondolaMeta

        for shelfMeta in GT.shelvesMeta:
            IDs = shelfMeta['id']
            gondolaID = IDs['gondola_id']['id']
            shelfID = IDs['shelf_index']
            shelfMetaIndexKey = str(gondolaID) + '_' + str(shelfID)
            self._shelvesDict[shelfMetaIndexKey] = shelfMeta

        for plateMeta in GT.platesMeta:
            IDs = plateMeta['id']
            gondolaID = IDs['shelf_id']['gondola_id']['id']
            shelfID = IDs['shelf_id']['shelf_index']
            plateID = IDs['plate_index']
            plateMetaIndexKey = str(gondolaID) + '_' + str(shelfID) + '_' + str(plateID)
            self._platesDict[plateMetaIndexKey] = plateMeta
        

    def getProductIDsFromPosition(self, *argv):
        gondolaIdx = argv[0] - 1
        if len(argv) == 2:
            shelfIdx = argv[1] - 1
            # remove Nones
            productIDs = set()
            for productIDSetForPlate in self._planogram[gondolaIdx][shelfIdx]:
                if productIDSetForPlate is None:
                    continue
                productIDs = productIDs.union(productIDSetForPlate)
            return productIDs
        if len(argv) == 3:
            shelfIdx = argv[1] - 1
            plateIdx = argv[2] - 1
            return self._planogram[gondolaIdx][shelfIdx][plateIdx]

    def getProductPositions(self, productID):
        product = self.getProductByID(productID)
        return product.positions

    def getTestStartTime(self):
        testCaseStartTimeJSONFilePath = './competition/TestCaseStartTime.json'
        if os.path.exists(testCaseStartTimeJSONFilePath):
            with open(testCaseStartTimeJSONFilePath, 'r') as f:
                testStartTime = json.load(f)
            if self.__dbname not in testStartTime:
                return 0
            return testStartTime[self.__dbname]
        else:
            print("!!!WARNING: Didn't find competition/TestCaseStartTime.json, results might not be accurate. Please run TimeTravel.py to get the json file")
            return 0

class Position:
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
    
    def __eq__(self, other):
        if isinstance(other, Position):
            return self.gondola == other.gondola and self.shelf == other.shelf and self.plate == other.plate
        else:
            return False
    
    def __hash__(self):
      return hash((self.gondola, self.shelf, self.plate))

class Coordinates: 
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def translateBy(self, delta_x, delta_y, delta_z):
        self.x += delta_x
        self.y += delta_y
        self.z += delta_z

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'Coordinates(%f, %f, %f)' % (self.x, self.y, self.z)

# class Frame:

"""
Class for customer target
Attributes:
    self.head: Coordinates. global coordinate of head position. Usage: Coordinates.x, Coordinates.y, Coordinates.z
    self.id: STRING. Identify of the target.
    self.score: FLOAT. Confidence score of the target existence.
    self.valid_entrance: BOOL. Whether this target is a valid entrance at the store.
"""
class Target:
    def __init__(self, id, head, left_hand=None, right_hand=None, valid_entrance=True):
        self.head = head
        self.id = id
        self.valid_entrance = valid_entrance

        self.left_hand = None
        self.right_hand = None
        if left_hand:
            self.left_hand = left_hand
        if right_hand:
            self.right_hand = right_hand
    
    def update(self, id, head, left_hand=None, right_hand=None, valid_entrance=True):
        self.head = head
        self.id = id
        self.valid_entrance = valid_entrance

        self.left_hand = None
        self.right_hand = None
        if left_hand:
            self.left_hand = left_hand
        if right_hand:
            self.right_hand = right_hand
    
    def __str__(self):
        return 'Target(ID: {})'.format(str(self.id))

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
