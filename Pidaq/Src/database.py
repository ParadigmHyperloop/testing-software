import csv
import datetime
import os

from influxdb import InfluxDBClient


class Influx:
    """Class to interact with the influx database

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

    def __format_data(self, data):
        """Formats data to be able to utilize in the Influx query

        Args:
            data(list(str)): List of data to be formatted

        Returns formatted_data(str): comma separated data in format
                                     '"data1","data2","data3"...'
        """
        list_data = []
        for d in data:
            list_data.append(f'"{d}"')
        formatted_data = ','.join(list_data)
        return formatted_data

    def switch_database(self, database):
        self.client.switch_database(database)
        self.current_database = database

    def log_data(self, data, measurement, tags):
        table_row = [{
            'measurement': measurement,
            'time': datetime.datetime.now(),
            'fields': data,
        }]
        self.client.write_points(table_row, tags=tags)

    def read_data(self, tags=[], measurements=[]):
        formatted_tags = self.__format_data(tags)
        formatted_measurements = self.__format_data(measurements)
        if len(measurements) == 0:
            data = self.client.query(
                f'SELECT {formatted_tags}',
                database=self.current_database
            )
        elif len(tags) == 0:
            data = self.client.query(
                f'SELECT * FROM {formatted_measurements}',
                database=self.current_database
            )
        else:
            data = self.client.query(
                f'SELECT {formatted_tags} FROM {formatted_measurements}',
                database=self.current_database
            )
        try:
            return (data.raw['series'])
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

    def export_to_csv(self, test_name, tags, measurements, csv_path):
        file_name = f'{test_name}.csv'
        data = self.read_data(tags=tags, measurements=measurements)
        with open(f'{csv_path}\\{file_name}', 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data[0]['columns'])
            for measurement in data:
                for row in measurement['values']:
                    writer.writerow(row)
