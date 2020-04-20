import json
from collections import namedtuple
from pymongo import MongoClient
import BookKeeper

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())
def json2obj(data): return json.load(data, object_hook=_json_object_hook)

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

with open('./store_meta/Gondolas.json') as f:
    gondolasMeta = json.load(f)['gondolas']
with open('./store_meta/Shelves.json') as f:
    shelvesMeta = json.load(f)['shelves']
with open('./store_meta/Plates.json') as f:
    platesMeta = json.load(f)['plates']
