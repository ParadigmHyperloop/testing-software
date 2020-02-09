# Example - Logging to Influx

Example of logging to influx using python, as well as how to setup influxdb. Drawn from http://richardn.ca/2019/01/04/installing-influxdb-on-windows/

## Installing nssm
nssm is the "non-sucking service manager", it is a valuable tool for creating, configuring, and deploying services on windows. It is simply an exe that has to be downloaded and then added to the PATH before it can be used from the CLI.

* Download here: https://nssm.cc/download
    
* Make a directory in program files called nssm and move the nssm.exe there
* Add C:/Program Files/nssm to your path
    * start -> "Edit system environment variables" -> environment variables path -> edit -> new -> path-to-nssm
* In console, type `nssm` to ensure it is installed corectly
___
## Setting Up Influxdb

### Windows
Download the V1.7.9 windows binaries here: <https://portal.influxdata.com/downloads/>

Extract the contents of the zip to a folder called `influxdb`, and place that folder in program files (doesnt really matter where tbh - I just used program files)

Create another directory anywhere you want to store the influx data, its recomended you do not place this folder within the same directory as the binaries. I called mine **`influx-data`**

Edit the following fields in the influx.conf file within the unzipped folder
* [meta] - dir: C:/Path to influx-data/meta
* [data] - dir: C:/Path to influx-data/data
* [data] - wal-dir: C:/Path to influx-data/wal

Next, we have to configure influx to run as a service. 
In an admin console:
* `nssm install` 
* Then configure the following settings with the correct paths (may differ from mine depending on where you put them) :
    * Path: c:\Program Files\influxdb\influxd.exe
    * Startup Directory: c:\Program Files\influxdb\
    * Arguments: -config "C:\Program Files\Iinfluxdb\influxdb.conf"
    * Service Name: influxdb

Finally, launch the service
```
nssm start influxdb
```

If all has gone well, go to http://localhost:8086/query\
And you should see something like:
``` 
{"error":"missing required parameter \"q\""}
```
