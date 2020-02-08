
# Control Laptop 
This directory contains code that will run on the control laptop. The laptop will:
-  Receive messages from the pi via UDP and         transmit commands via TCP. 
- Store the receieved data in influxdb.
- Serve grafana and influx
- Communicate with the control GUI via socketio 

## DataLogger
Generic name for python application that will log incoming data into influxdb

***
## DataShuttle

Generic name for python application that will recieve and parse incoming CAN messages - as well as send commands.

***
## Examples

Includes relevant examples for some python modules, influx, and grafana configuration

***
## Services

Includes the configuration and documentation for the grafana server and influxdb
