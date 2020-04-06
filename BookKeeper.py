import numpy as np
from pymongo import MongoClient
from collections import namedtuple

class BookKeeper:

    def __init__(self):
        mongoClient = MongoClient('localhost:27017')
        self.db = mongoClient['cps-test-2']

        DBs = namedtuple('DBs', 'planogramDB, productsDB, plateDB')
        self.DBs = DBs(planogramDB=self.db['planogram'], productsDB=self.db['products'], plateDB=self.db['plate_data'])

        self.planogram = self.loadPlanogram()
        self.products = self.loadProducts()

    def loadPlanogram(self):
        num_gondola = 5
        num_shelf = 6
        num_plate = 12
        planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)
        planogramDB = self.DBs.planogramDB


        for item in planogramDB.find():
            for plate in item['plate_ids']:
                shelf = plate['shelf_id']
                gondola = shelf['gondola_id']
                gondolaID = gondola['id']
                shelfID = shelf['shelf_index']
                plateID = plate['plate_index']

                planogram[gondolaID-1][shelfID-1][plateID-1] = item['planogram_product_id']['id']

        return planogram

    def loadProducts(self):
        return None