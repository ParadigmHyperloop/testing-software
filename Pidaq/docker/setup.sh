# sudo apt-get update
# sudo apt-get upgrade -y
cd $HOME/Desktop/
FILE=testing-software/
if [ -d "$FILE" ]
then
	echo "$REPO repository already exists."
else
	git clone https://github.com/ParadigmHyperloop/testing-software.git
fi

if ! [ -x "$(command -v docker)" ]; then
	curl -fsSL https://get.docker.com -o get-docker.sh
	sudo sh get-docker.sh
fi

sudo docker pull influxdb
sudo docker pull grafana/grafana
