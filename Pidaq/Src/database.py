import datetime
import os

from influxdb import InfluxDBClient

class Influx:
    """
    """

    def __init__(self, database):
        self.client = InfluxDBClient(host='localhost', port=8086)
        self.client.create_database() #TODO figure out why environment variable is used here
         
    def log_data(self, data):
        table_row =[{
            'measurement': 'sensor_data',
            'time': datetime.datetime.now(),
            'fields': data
        }]
        self.client.write_points(table_row)

    def switch_database(self, database):
        pass