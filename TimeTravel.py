import json
import requests
import os
import zipfile
from datetime import datetime
import subprocess

with open('./competition/day1-tests.json') as f:
    testCases = json.load(f)



videosDir = './videos/'

archivesDir = './archives/'
if os.path.exists(archivesDir) != True:
    os.mkdir(archivesDir)



with open('./TestCaseStartTime.json') as f:
    testCaseStartTime = json.load(f)


for testCase in testCases:
    archives = testCase['archives']
    name = testCase['name']

    if name not in testCaseStartTime:
        videos = testCase['videos']
        videosDir = videosDir + name + '/'
        if os.path.exists(videosDir):
            print('have video already')
        else:
            os.mkdir(videosDir)
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
                for videoName in os.listdir(videosDir + name):
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
        continue
    for url in archives:
        if url.endswith('.archive'):
            newUrl = url.replace('cloud.google', 'googleapis')
            print(newUrl)
            r = requests.get(newUrl)
            open(archivePath, 'wb').write(r.content)
            dbRestoreCommand = 'mongorestore --archive=' + archivePath
            proc = subprocess.Popen([dbRestoreCommand], stdout=subprocess.PIPE, shell=True) 
            (out, err) = proc.communicate()

with open('TestCaseStartTime.json', 'w') as f:
    json.dump(testCaseStartTime, f)
        
    
    

