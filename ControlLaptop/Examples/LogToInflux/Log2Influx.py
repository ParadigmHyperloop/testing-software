# Example for logging data to influxdb using python
# Sourced from the influxdb python docs

import random
import time
from datetime import datetime 
from influxdb import InfluxDBClient

# Example data payload
# Tags contain metadata about the measurement - always a string
# Thinking we could have something like below for each measurement

def main():
        
    telemetry = [
        {
            "measurement": "temperature",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            #"time": f"{datetime.now()}",
            "fields": {
                "Celsius": 1.0,
                "Fahrenheit": 3,
            }
        }
    ]

    # Create client instance
    # host, port, user, pass, database
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

    # Create a new database in influx
    client.drop_database('example')
    client.create_database('example')

    while 1:

        print(f"C: {telemetry[0]['fields']['Celsius']}")
        print(f"F: {telemetry[0]['fields']['Fahrenheit']}")
        print()

        # Writing the payload to the DB
        client.write_points(telemetry)

        # Scramble data
        telemetry[0]['fields']['Celsius'] = random.random() * 100.0 
        telemetry[0]['fields']['Fahrenheit'] = random.randint(0,100) 

        time.sleep(1)

    # Print the results of the query
    result = client.query('select Celsius,Fahrenheit from temperature;')
    print(f"Inserted: {result}")
    print()

if __name__ == "__main__":
    main()