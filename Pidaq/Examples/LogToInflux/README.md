# Example - Logging to Influx

Example of logging to influx using python, as well as how to setup influxdb and grafana. Drawn from http://richardn.ca/2019/01/04/installing-influxdb-on-windows/



## Installing nssm
nssm is the "non-sucking service manager", it is a valuable tool for creating, configuring, and deploying services on windows. It is simply a .exe that is downloaded and then added to the PATH before it can be used from the CLI (Command line interface).

* Download here: https://nssm.cc/download
    
* Make a directory in program files called nssm and move the nssm.exe there
* Add C:/Program Files/nssm to your path
    * start -> "Edit system environment variables" -> environment variables path -> edit -> new -> path-to-nssm

* In console, enter `nssm` to ensure it is installed correctly


## Setting Up Influxdb

### Windows
Download the V1.7.9 windows binaries here: <https://portal.influxdata.com/downloads/>

Extract the contents of the zip to a folder called `influxdb`, and place that folder in program files (doesnt really matter where - I just used program files)

Create another directory anywhere you want to store the influx data, its recommended you do not place this folder within the same directory as the binaries. I called mine **`influx-data`**

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
You can now enter the influx interactive shell by navigating to the influxdb folder containing `influx.exe` and running it (enter `influx` in console or double click the exe)


## Setting Up Grafana
### Windows
This pretty much describes everything you need to  know in a concise and visual form, no need to reinvent the wheel. 
<https://devconnected.com/how-to-install-grafana-on-windows-8-10/>

Note: It is not necessary to use a custom .ini, the defaults are fine for most use cases! There will be a config file for the production grafana server that we will use, however for personal dev environments the defaults are fine.

After getting grafana running as a service, you can login and import the dashboard by uploading the ` dashboard.json` file in this directory.




