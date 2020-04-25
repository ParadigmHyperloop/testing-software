import csv
import datetime
import os

from influxdb import InfluxDBClient


class Influx:
    """Class to interact with the influxdb

    This class enables interaction with the influx time series database through
    the use of the api. The class also enables the ability to export test
    results to a csv file, for postprocessing and analysis/

    Attributes:
        client (InfluxDBClient): Instance of InfluxDB api to interact with the 
                                 database
        current_database (str): Current database that the class is interacting 
                                with
    """

    def __init__(self, database):
        """
        Args:
            database (str): Name of database to connect to. If the database
                            does not exist, it will be created.
        """
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
        try:
            return (data.raw['series'][0])
        except KeyError:
            return

    def create_retention_policy(self, name, duration, replication):
        self.client.create_retention_policy(
            name,
            duration,
            replication,
            database=self.current_database,
            default=True
        )

    def export_to_csv(self, test_name, csv_path):
        file_name = f'{test_name}.csv'
        data = self.read_data(tags=test_name)
        with open(f'{csv_path}/{file_name}', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data['columns'])
            for row in data['values']:
                writer.writerow(row)

