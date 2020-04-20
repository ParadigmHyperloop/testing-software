# Example for logging data to influxdb using python
# Sourced from the influxdb python docs

import random
import time
from datetime import datetime 

from influxdb import InfluxDBClient

# Example data payload
# Tags contain metadata about the measurement - always a string

def main():
        
    telemetry = [
           {
            "measurement": "temperature",
            "tags": {
                "host": "server01",
                "region": "us-west"
            }
            "fields": {
                "Celsius": 1.0,
                "Fahrenheit": 3,
               }
           },
        
          {
            "measurement": "pressure",
            "tags": {
                "host": "server01",
                "region": "us-west",
                "config": "1",
            },
            "fields": {
                "millibar": 1.0,
                "Pascal": 3.0,
                }
           },
         
         {
            "measurement": "Height",
            "tags": {
                "host": "server01",
                "region": "us-west",
                "config": "1",
            },
            "fields": { 
                "Metre": 1.0,
                "Feet": 3.0,
                }
           },
         
         {
            "measurement": "samplem1",
            "tags": { 
                "host": "server01",
                "region": "us-west",
                "config": "1",
            },
            "fields": {
                "samplef01": 10,
                "samplef02": 31,
                "samplef03": 12,
                }
         },
           
         {
            "measurement": "samplem2",
            "tags": { 
                "host": "server01",
                "region": "us-west",
                "config": "1",
            },
            "fields": {
                "samplef11": 9.0,
                "samplef12": 36,
                "samplef13": 1,
                }
         },
           
         {
            "measurement": "samplem3",
            "tags": { 
                "host": "server01",
                "region": "us-west",
                "config": "1",
            },
            "fields": {
                "samplef21": 8,
                "samplef22": 12,
                "samplef23": 16,
                }
         },
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
        print(f"mbar: {telemetry[1]['fields']['millibar']}")
        print(f"Pa: {telemetry[1]['fields']['Pascal']}")
        print(f"m: {telemetry[2]['fields']['Metre']}")
        print(f"ft: {telemetry[2]['fields']['Feet']}")
        print(f"s01: {telemetry[3]['fields']['samplef01']}")
        print(f"s02: {telemetry[3]['fields']['samplef02']}")
        print(f"s03: {telemetry[3]['fields']['samplef03']}")
        print(f"s11: {telemetry[4]['fields']['samplef11']}")
        print(f"s12: {telemetry[4]['fields']['samplef12']}")
        print(f"s13: {telemetry[4]['fields']['samplef13']}")
        print(f"s21: {telemetry[5]['fields']['samplef21']}")
        print(f"s22: {telemetry[5]['fields']['samplef22']}")
        print(f"s23: {telemetry[5]['fields']['samplef23']}")
        print()
        
        # Writing the payload to the DB
        client.write_points(telemetry)

        # Scramble data
        telemetry[0]['fields']['Celsius'] = random.random() * 100.0 
        telemetry[0]['fields']['Fahrenheit'] = random.randint(0,100)
        telemetry[1]['fields']['millibar'] = random.gauss(1,0.5)
        telemetry[1]['fields']['Pascal'] = random.gauss(100,5)
        telemetry[2]['fields']['Metre'] = random.gauss(60,5) 
        telemetry[2]['fields']['Feet'] = random.gauss(23,7)
        telemetry[3]['fields']['samplef01'] = random.randint(60,65)
        telemetry[3]['fields']['samplef02'] = random.randint(70,75)
        telemetry[3]['fields']['samplef03'] = random.randint(90,95)
        telemetry[4]['fields']['samplef11'] = random.gauss(5,5)
        telemetry[4]['fields']['samplef12'] = random.randint(100,105)
        telemetry[4]['fields']['samplef13'] = random.randint(20,25)
        telemetry[5]['fields']['samplef21'] = random.randint(10,15)
        telemetry[5]['fields']['samplef22'] = random.randint(30,35)
        telemetry[5]['fields']['samplef23'] = random.randint(130,135)
        
        time.sleep(1)

    # Print the results of the query
    result = client.query('select Celsius,Fahrenheit from temperature;')
    print(f"Inserted: {result}")
    result2 = client.query('select millibar,Pascal from pressure;')
    print(f"Inserted: {result2}")
    result3 = client.query('select Metre,Feet from Height;')
    print(f"Inserted: {result3}")
    result4 = client.query('select samplef01,samplef02,samplef03 from samplem1;')
    print(f"Inserted: {result4}")
    result5 = client.query('select samplef11,samplef12,samplef13 from samplem2;')
    print(f"Inserted: {result5}")
    result6 = client.query('select samplef21,samplef22,samplef23 from samplem3;')
    print(f"Inserted: {result6}")
    print()

if __name__ == "__main__":
    main()
