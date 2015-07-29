#!/bin/bash

cd "$(dirname "$0")"

# Установка docker

sudo apt-get update -y
sudo apt-get install wget
wget -qO- https://get.docker.com/ | sh

# установка mongo

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list

sudo apt-get update -y

sudo apt-get install -y mongodb-org

sudo apt-get install -y mongodb-org=3.0.5 mongodb-org-server=3.0.5 mongodb-org-shell=3.0.5 mongodb-org-mongos=3.0.5 mongodb-org-tools=3.0.5

echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

# Установка nodejs
sudo apt-get install -y nodejs npm node

cd service_prototype/
npm install --save mongodb

cd ..
# Установка модулей для программ на питоне
sudo apt-get install python3-pip -y
sudo apt-get install python3-tk
sudo pip3 install python-dateutil
sudo pip3 install pymongo