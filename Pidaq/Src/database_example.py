import json
import os

from database import Influx

database = Influx('example')

# Print data from pressure measurement in formatted json
data = database.read_data(tags=['millibar', 'Pascal'], measurements=['pressure'])
print(data)

# Export example data to a csv
cwd = os.getcwd()
database.export_to_csv('test', [], ['pressure', 'temperature'], cwd)

# Log new data to the database, and print to console
data = {
    'Celcius': 30.21,
    'Fahrenheit': 87
}
tags = {
    'host': 'server01',
    'region': 'us-east'
}
database.log_data(data, 'temperature', tags)
new_data = database.read_data(tags=['Celcius', 'Fahrenheit'], measurements=['temperature'])
print(new_data)
