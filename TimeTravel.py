import json
import requests
import os
import zipfile
from datetime import datetime
import subprocess

# GET test cases
headers = {
    'TOKEN': '5ea023be-b530-4816-8eda-5340cfabe9b0'
}
response = requests.get(url='http://cps-week.internal.aifi.io/api/v1/testcases', headers=headers)

testCases = []
if response.status_code == 200:
    responsStr = response.content
    testCases = json.loads(responsStr)
    with open('competition/test_cases.json', 'w') as f:
        json.dump(testCases, f)



videosDir = './videos/'
if os.path.exists(videosDir) != True:
    os.mkdir(videosDir)

archivesDir = './archives/'
if os.path.exists(archivesDir) != True:
    os.mkdir(archivesDir)


testCaseJSONFilePath = './competition/TestCaseStartTime.json'
testCaseStartTime = {}
if os.path.exists(testCaseJSONFilePath):
    with open(testCaseJSONFilePath) as f:
        testCaseStartTime = json.load(f)


for testCase in testCases:
    archives = testCase['archives']
    name = testCase['name']
    if name not in testCaseStartTime:
        videos = testCase['videos']
        dirForCurrentTestCase = videosDir + name
        if os.path.exists(dirForCurrentTestCase):
            print('have videos already, ', dirForCurrentTestCase)
        else:
            for url in videos:
                if url.endswith('Videos.zip'):
                    newUrl = url.replace('cloud.google', 'googleapis')
                    print(newUrl)
                    r = requests.get(newUrl)
                    zipPath = videosDir + 'Videos.zip'
                    open(zipPath, 'wb').write(r.content)
                    with zipfile.ZipFile(zipPath,"r") as zip_ref:
                        zip_ref.extractall(videosDir)
                    os.unlink(zipPath)
        timestamps = []
        for videoName in os.listdir(dirForCurrentTestCase):
            # print(videoName)
            split1 = videoName.split('_')
            dateStr, fooTimeStr = split1[1], split1[2]
            timeStr = fooTimeStr.split('.')[0]
            completeTimeStr = dateStr + '_' + timeStr + ' +0200'
            # '2020-04-20_07-33-37'
            datetimeObj = datetime.strptime(completeTimeStr, '%Y-%m-%d_%H-%M-%S %z')
            timestamps.append(datetimeObj.timestamp())
        timestamps.sort()
        testCaseStartTime[name] = timestamps[0]
        print(testCaseStartTime)

    archivePath = archivesDir + name + '.archive'
    if os.path.exists(archivePath):
        print("already have archive ", archivePath)
    else:
        for url in archives:
            if url.endswith('.archive'):
                newUrl = url.replace('cloud.google', 'googleapis')
                print(newUrl)
                r = requests.get(newUrl)
                open(archivePath, 'wb').write(r.content)
                dbRestoreCommand = 'mongorestore --archive=' + archivePath
                proc = subprocess.Popen([dbRestoreCommand], stdout=subprocess.PIPE, shell=True) 
                (out, err) = proc.communicate()

with open(testCaseJSONFilePath, 'w') as f:
    json.dump(testCaseStartTime, f)
        
    
    

