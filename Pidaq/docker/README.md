# Raspbian Docker Setup
**Developed by Mark Duffett for CompV Software**

Building and running the raspbian docker container:

* Docker build
```
docker build -t pidaq:v1 .
```

* Docker Run (open to bash prompt)
```
docker run -it -v path-to-PIDAQ-dir:/home/data pidaq:v1 /bin/bash
```

* Docker Run (launch script)
```
docker run -it -v path-to-PIDAQ-dir:/home/data --entrypoint helloTest.sh pidaq:v1
```

*Where path-to-PIDAQ-dir = `/c/Hyperloop/testing-software/Pidaq on my machine*

## General Docker Commands
* `docker --version` // Check docker version/ ensure docker is installed
* `docker image ls` // list docker images

## Remote Pi SSH Setup
* `sudo systemctl enable ssh`
* `sudo systemctl start ssh`
* `ifconfig` // to get IP address of raspi

Default: user=pi, password=raspberry

