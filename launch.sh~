#!/bin/bash

cd /home/natasha/Документы/project
for ((x=1; x<3; x++)) do
	docker run --name influxdb_${x} -d usr/influxdb
	docker run -v $(pwd)/collectd/collectd_${x}.conf:/etc/collectd/collectd.conf \
	--name collectd_${x} --link influxdb_${x} -d usr/collectd
	echo $((x+3000))
	docker run -v $(pwd)/node/u3/handlers/vals_${x}.js:/src/handlers/vals.js \
	-p $((x+3000)):3000 --name node_${x} --link influxdb_${x} -d usr/node
done

