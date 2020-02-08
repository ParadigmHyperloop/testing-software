# Pidaq (Raspberry Pi Data Aquisitor) 

This directory contains all of the code that will run on the raspberry pi. The pi will receive and parse CAN messages, and create either a JSON or protobuf message to send to the control laptop via ethernet (UDP)
*** 

## DataLogger
Generic name for python application that will log incoming data into influxdb

***
## DataShuttle

Generic name for python application that will recieve and parse incoming CAN messages

***
## Examples

Includes relevant examples for some python modules, influx, and grafana configuration

***
## Services

Includes the configuration and documentation for the grafana server and influxdb
