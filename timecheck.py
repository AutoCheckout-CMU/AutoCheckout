from pymongo import MongoClient
import json


testCaseJSONFilePath = './competition/TestCaseStartTime.json'
with open(testCaseJSONFilePath) as f:
    testCaseStartTime = json.load(f)

mongoClient = MongoClient('mongodb://localhost:27017')
for dbName in testCaseStartTime:
    db = mongoClient[dbName]
    plateDataDB = db['plate_data']
    timestamp = plateDataDB.find_one(sort=[("timestamp", 1)])["timestamp"]
    print(dbName, ': videoTime=', testCaseStartTime[dbName], 'dbTime=', timestamp, testCaseStartTime[dbName] - timestamp)