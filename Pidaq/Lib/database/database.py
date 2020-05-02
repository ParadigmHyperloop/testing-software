"""Contains class to interface with the influx database

Classes:
    Influx: contains methods which allows data to be queried, read, and
            exported to a csv file. Tags, measurements, and fields can
            be specified, and data retention policies can be created.

Functions:
    format_data: Formats data in the correct way to pass the data into a query
                 string in the Influx class
"""

import csv
from datetime import datetime
import os

from influxdb import InfluxDBClient


class Influx:
    """Class to interact with the influx database

    This class enables interaction with the influx time series database through
    the use of the api. The class also enables the ability to export test
    results to a csv file, for postprocessing and analysis

    Attributes:
        client (InfluxDBClient): Instance of InfluxDB api to interact with the
                                 database
        current_database (str): Current database that the class is interacting
                                with
    """

    def __init__(self, database: str, host: str, port: int) -> None:
        """

        Args:
            database (str): Name of database to connect to. If the database
                            does not exist, it will be created.
        """

        self.client = InfluxDBClient(host=host, port=port)
        current_databases = self.client.get_list_database()
        if not any(current_database['name'] == database
                   for current_database in current_databases):
            self.client.create_database(database)
        self.client.switch_database(database)
        self.current_database = database

    def switch_database(self, database: str) -> None:
        """Switches currently active database"""

        current_databases = self.client.get_list_database()
        if not any(self.current_database['name'] == database
                   for self.current_database in current_databases):
            self.client.create_database(database)
        self.client.switch_database(database)
        self.current_database = database

    def log_data(self, data: dict, measurement: str, tags: dict) -> None:
        """Logs a single data point to the database"""

        table_row = [{
            'measurement': measurement,
            'time': datetime.now(),
            'fields': data,
        }]
        self.client.write_points(table_row, tags=tags)

    def read_data(self, query=None, tags=None, fields=None, measurements=None) -> str:
        """Reads database for specified measurements, including specified tags and fields
        
        Format of a query when not using query parameter:
            SELECT fields FROM measurements WHERE tags.keys = tags.values
        
        Args:
            query (str): if argument is passed, all other parameters are ignored, and database
                         is queried
            tags (dict): Contains the tag keys and values to be included in the query
            fields (list(str)): Contains fields to be queried
            measurements (list(str)): Contains the measurements to be queried from

        Returns:
            (str) Raw json data
        """

        if query is not None:
            data = self.client.query(query, database=self.current_database)
        elif measurements is None:
            return -1
        else:
            formatted_measurements = ','.join([f'"{measurement}"' for measurement in measurements])
            formatted_fields = ','.join([f'"{field}"' for field in fields]) if fields is not None else '*'
            if tags is None:
                self.client.query(
                    f'SELECT {formatted_fields} FROM {formatted_measurements}',
                    database=self.current_database
                )
            else:
                formatted_tags = ' AND '.join(f'{key} = {value}' for key, value in tags.items())
                self.client.query(
                    f'SELECT {formatted_fields} FROM {formatted_measurements} WHERE {formatted_tags}',
                    database=self.current_database
                )
        try:
            return data.raw['series']
        except KeyError:
            return -1

    def create_retention_policy(self, name: str, duration: str, replication: str) -> None:
        """Creates a retention policy for the current database"""

        self.client.create_retention_policy(
            name,
            duration,
            replication,
            database=self.current_database,
            default=True
        )

    def export_to_csv(self, test_name: str,
                            query=None,
                            tags=None,
                            fields=None,
                            measurements=None,
                            csv_path=None) -> None:
        """Exports measurements to a csv file

        Args:
            test_name (str): Name of test, becomes name of csv file
            query (str): manually specify exact query for data to be included in csv
            tags (list(str)): Tags and fields to be included in csv
            measurements (list(str)): Measurements to be included in csv
            csv_path(str): File path of where the csv will be written
        """
        
        date_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
        file_name = f'{test_name}_{date_time}.csv'
        if query is None:
            data = self.read_data(tags=tags, fields=fields, measurements=measurements) 
        else:
            data = self.read_data(query=query)
        if csv_path is None:
            csv_path = os.getcwd()
        with open(os.path.join(csv_path, file_name), 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data[0]['columns'])
            for measurement in data:
                for row in measurement['values']:
                    writer.writerow(row)
        

def create_metadata_file(test_name: str, operator_name: str, commands: list, path=None) -> None:
    """Creates a file containing metadata about the current test"""

    date_time = datetime.now().strftime("%d-%m-%Y_%H:%M")
    file_name = f'{test_name}_{date_time}.info'
    if path is None:
        file_path = os.getcwd()
    with open(os.path.join(path, file_name), 'w', newline='\n') as infofile:
        infofile.write(f'Test: {test_name}\n')
        infofile.write(f'Date: {date_time}\n')
        infofile.write(f'Test operated by: {operator_name}\n')
        infofile.write(f'List of commands:\n{'\n'.join(commands)}')
        infofile.close()


if __name__ == "__main__": # TODO tidy up testing
    # Testing class functionality

    DATABASE = Influx('example', 'localhost', 8086)

    # Print data from pressure measurement in formatted json
    print(DATABASE.read_data(tags=['millibar', 'Pascal'], measurements=['pressure']))

    # Export example data to a csv
    CWD = os.getcwd()
    DATABASE.export_to_csv('test', measurements=['pressure', 'temperature'])

    # Log new data to the database, and print to console
    FIELDS = {
        'Celcius': 30.21,
        'Fahrenheit': 87
    }
    TAGS = {
        'host': 'server01',
        'region': 'us-east'
    }
    DATABASE.log_data(FIELDS, 'temperature', TAGS)
    print(DATABASE.read_data(fields=['Celsius', 'Fahrenheit'], measurements=['temperature']))

    # Switch to a new database, and log some data
    DATABASE.switch_database('example1')
    for i in range(10):
        DATABASE.log_data(FIELDS, 'temperature', TAGS)

    # Testing that a new database is not created if one of the same name already exists
    SECOND_DATABASE = Influx('example1', 'localhost', 8086)
    print(SECOND_DATABASE.read_data(measurements=['temperature']))

    # Testing creating new database on construction of class instance
    THIRD_DATABASE = Influx('example2', 'localhost', 8086)

    # Testing creating new database using switch_database method
    THIRD_DATABASE.switch_database('example3')
    print(THIRD_DATABASE.client.get_list_database())
