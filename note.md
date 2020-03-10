mongo mongodb://cpsweek:localdb@localhost:27018
docker ps
mongo mongodb://cpsweek:localdb@localhost:27018
show dbs
use cps-test-01
db
show collections
db.frame_message.count()
db.frame_message.find().limit(1).pretty()
docker-compose run cpsdriver
docker-compose run mongodb
docker-compose stop mongodb
AIFI_CPSWEEK_COMP__COMMAND=cps-test-01 docker-compose up --build


# work with depth data

## work with mongodb directly
brew install  mongodb-community
brew services start mongodb-community
mongorestore --archive=/Users/mzhang/git-clones/AutoCheckout-CMU-F4/data/downloads/cps-test-01-all.archive
mongo
show dbs
use cps-test-01
db.plate_data.find().limit(1).pretty()
brew services stop mongodb-community  

## docker not working
AIFI_CPSWEEK_COMP__COMMAND=cps-test-01 AIFI_CPSWEEK_COMP__SAMPLE=all docker-compose up --build

cpsdriver_1  | Traceback (most recent call last):
cpsdriver_1  |   File "cpsdriver/main.py", line 43, in <module>
cpsdriver_1  |     main(args=sys.argv[1:])
cpsdriver_1  |   File "cpsdriver/main.py", line 22, in main
cpsdriver_1  |     test_client.load(f"{args.command}-{args.sample}")
cpsdriver_1  |   File "/app/cpsdriver/clients.py", line 249, in load
cpsdriver_1  |     return self.cps_mongo_client.load_archive(archive)
cpsdriver_1  |   File "/app/cpsdriver/clients.py", line 120, in load_archive
cpsdriver_1  |     return mongorestore(uri=self.uri, archive=filepath)
cpsdriver_1  |   File "/usr/local/lib/python3.8/site-packages/sh.py", line 1427, in __call__
cpsdriver_1  |     return RunningCommand(cmd, call_args, stdin, stdout, stderr)
cpsdriver_1  |   File "/usr/local/lib/python3.8/site-packages/sh.py", line 774, in __init__
cpsdriver_1  |     self.wait()
cpsdriver_1  |   File "/usr/local/lib/python3.8/site-packages/sh.py", line 792, in wait
cpsdriver_1  |     self.handle_command_exit_code(exit_code)
cpsdriver_1  |   File "/usr/local/lib/python3.8/site-packages/sh.py", line 815, in handle_command_exit_code
cpsdriver_1  |     raise exc
cpsdriver_1  | sh.SignalException_SIGKILL: 
cpsdriver_1  | 
cpsdriver_1  |   RAN: /usr/bin/mongorestore --uri=mongodb://cpsweek:localdb@mongodb:27017 --archive=data/downloads/cps-test-01-all.archive
cpsdriver_1  | 
cpsdriver_1  |   STDOUT:
cpsdriver_1  | 
cpsdriver_1  | 
cpsdriver_1  |   STDERR:
cpsdriver_1  | 2020-02-25T01:16:16.793+0000     preparing collections to restore from
cpsdriver_1  | 2020-02-25T01:16:16.808+0000     reading metadata for cps-test-01.plate_data from archive 'data/downloads/cps-test-01-all.archive'
cpsdriver_1  | 2020-02-25T01:16:16.821+0000     restoring cps-test-01.plate_data from archive 'data/downloads/cps-test-01-all.archive'
cpsdriver_1  | 2020-02-25T01:16:16.920+0000     restoring indexes for collection cps-test-01.plate_data from metadata
cpsdriver_1  | 2020-02-25T01:16:16.946+0000     finished restoring cps-test-01.plate_data (842 documents, 0 failures)
cpsdriver_1  | 2020-02-25T01:16:16.947+0000     reading metadata for cps-test-01.targets from archive 'data/downloads/cps-test-01-all.archive'
cpsdriver_1  | 2020-02-25T01:16:16.968+0000     restoring cps-test-01.targets from archive 'data/downloads/cps-test-01-all.archive'
cpsdriver_1  | 2020-... (3328 more, please see e.stderr)
mongodb_1    | 2020-02-25T01:17:14.342+0000 I  NETWORK  [conn1] end connection 172.20.0.3:47588 (1 connection now open)
mongodb_1    | 2020-02-25T01:17:14.343+0000 I  NETWORK  [conn2] end connection 172.20.0.3:47590 (0 connections now open)
autocheckout-cmu-f4_cpsdriver_1 exited with code 1



