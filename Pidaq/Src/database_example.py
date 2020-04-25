import json

from database import Influx

database = Influx('example')

# Print data from pressure measurement in formatted json
data = database.read_data(tags=['millibar', 'Pascal'], measurements=['pressure'])
parsed_data = json.loads(data)
print(json.dumps(parsed_data, indent=2, sort_keys=True))
