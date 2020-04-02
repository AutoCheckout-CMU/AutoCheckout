# general env
git config --global user.name "Mengmeng ZHANG"
git config --global user.email "qiuyu8290@gmail.com"

# virtual env
python3 -m venv env
source env/bin/activate
pip install --user ipykernel
python3 -m ipykernel install --user --name=env
=> Installed kernelspec env in /Users/mzhang/Library/Jupyter/kernels/env
vim /Users/mzhang/Library/Jupyter/kernels/env/kernel.json
jupyter kernelspec list
jupyter kernelspec uninstall venv

pip install -r requirements.txt
deactivate

# mongodb in docker
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

# mongodb mac
brew install  mongodb-community
brew services start mongodb-community
mongorestore --archive=/Users/mzhang/git-clones/AutoCheckout-CMU-F4/data/downloads/cps-test-01-all.archive
mongo
show dbs
use cps-test-01
db.plate_data.find().limit(1).pretty()
brew services stop mongodb-community

client = MongoClient('mongodb://localhost:27017')

# mongodb linux
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
mongorestore --archive=/home/ubuntu/git-clones/AutoCheckout-CMU-F4/data/downloads/cps-test-01-all.archive
mongo

# monitor
sudo iotop
sudo nethogs

# tmux
tmux new -s s0
tmux attach -t s0
detach: ctrl+b d