import csv
import datetime
import os

from influxdb import InfluxDBClient


class Influx:
    """
    """

    def __init__(self, database):
        self.client = InfluxDBClient(host='localhost', port=8086)
        self.current_database = database
        current_databases = self.client.get_list_database()
        if not any(current_database['name'] == database for current_database in current_databases):
            self.client.create_database(database)
        self.client.switch_database(database)

    def switch_database(self, database):
        self.client.switch_database(database)

    def log_data(self, data, tags):
        table_row = [{
            'measurement': 'sensor_data',
            'time': datetime.datetime.now(),
            'fields': data,
        }]
        self.client.write_points(table_row, tags=tags)

    def read_data(self, tags='*', measurements=None):
        tags_formatted = []
        measurements_formatted = []
        for tag in tags:
            tags_formatted.append(f'"{tag}"')
        for measurement in measurements:
            measurements_formatted.append(f'"{measurement}"')
        tags_all = ','.join(tags_formatted)
        measurements_all = ','.join(measurements_formatted)
        if measurements == None:
            data = self.client.query(
                f'SELECT {tags_all}',
                database=self.current_database
            )
        else:
            data = self.client.query(
                f'SELECT {tags_all} FROM {measurements_all}',
                database=self.current_database
            )
        return data

    def create_retention_policy(self, name, duration, replication):
        self.client.create_retention_policy(
            name,
            duration,
            replication,
            database=self.current_database,
            default=True
        )

    def export_csv(self):
        
