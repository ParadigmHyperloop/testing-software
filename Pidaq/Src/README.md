# Database Interface Example
- This program tests the functionality of the database interface class (Influx) utilizing the database created when the `log-windtunnel-influx` python script is ran.

## Utilization
- Set up Influxdb on your machine using the README in `ControlLaptop/Examples/LogToInflux`
- Run the `log-windtunnel-influx.py` script, this will create an example database, and fill it with data points
- Run the `database_example.py` script, this will do three things:
    1. Read the pressure measurements from the example database, and print them in json format to the console
    2. Read the pressure and temperature measurements from the example database, and write them to a csv file called `test.csv` located in the directory from which the script is run
    3. Log a temperature data point to the database, and print the temperature measurement to the console in json format, the new data point should now be visible