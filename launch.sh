#!/bin/bash


cd "$(dirname "$0")"

for ((x=1; x<3; x++)) do
	sudo docker run --name influxdb_${x} -d usr/influxdb
	sudo docker run -v $(pwd)/collectd/collectd_${x}.conf:/etc/collectd/collectd.conf \
	-v /home/$USER/csv_${x}/:/var/lib/collectd/csv/ \
	--name collectd_${x} --link influxdb_${x} -d usr/collectd
	echo $((x+3000))
	sudo docker run -v $(pwd)/node/u3/handlers/vals_${x}.js:/src/handlers/vals.js \
	-p $((x+3000)):3000 --name node_${x} --link influxdb_${x} -d usr/node
done

