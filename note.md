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

