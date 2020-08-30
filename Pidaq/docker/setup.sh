#!/bin/bash
sudo apt-get update
sudo apt-get upgrade -y

cd $HOME/Desktop/
FILE=testing-software/

if [ -d "$FILE" ]
then
	echo "$FILE repository already exists."
else
	git clone https://github.com/ParadigmHyperloop/testing-software.git
fi

if ! [ -x "$(command -v docker)" ]; then
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
fi

sudo docker pull influxdb
sudo docker pull grafana/grafana


if docker run -d --name=influxdb -p 8086:8086 -v /var/lib/influxdb:/var/lib/influxdb influxdb
then
	echo "created influxdb container" 
else
	docker start influxdb
fi

if docker run -d --name=grafana -p 3000:3000 grafana/grafana
then
	echo "created grafana container" 
else
	docker start grafana
fi
