#!/bin/bash

docker build -t usr/influxdb ./influxdb
docker build -t usr/collectd ./collectd
docker build -t usr/node ./node

