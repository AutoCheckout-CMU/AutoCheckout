import numpy as np

class DataManager:

    def __init__(self, db):
        self.db = db
        self.planogram = self.loadPlanogram()

    def loadPlanogram(self):
        num_gondola = 5
        num_shelf = 6
        num_plate = 12
        planogram = np.empty((num_gondola, num_shelf, num_plate), dtype=object)
        planogramDB = self.db['planogram']


        for item in planogramDB.find():
            for plate in item['plate_ids']:
                shelf = plate['shelf_id']
                gondola = shelf['gondola_id']
                gondolaID = gondola['id']
                shelfID = shelf['shelf_index']
                plateID = plate['plate_index']

                planogram[gondolaID-1][shelfID-1][plateID-1] = item['planogram_product_id']['id']

        return planogram

    