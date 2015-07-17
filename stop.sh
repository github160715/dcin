#!/bin/bash

for ((x=1; x<3; x++)) do
docker stop node_${x} influxdb_${x} collectd_${x}
docker rm node_${x} influxdb_${x} collectd_${x}
done


