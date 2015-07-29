#!/bin/bash

cd "$(dirname "$0")"

sudo docker build -t usr/influxdb ./influxdb
sudo docker build -t usr/collectd ./collectd
sudo docker build -t usr/node ./node

