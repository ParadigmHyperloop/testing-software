# Can Manager
This package contains classes and functions required to interface with the can bus that will be used for data acquisition from the sensor board, and control
## Contents
- `can_manager.py` - module containing CanManager class, and SensorReading class for storing information about each sensor reading
- `message_config.json` - this file will be populated with the sensor reading configurations for each project. It will contain the can message id, reading name, conversion factor and conversion factor type.
- `example_message_config.json` - used for the test case
## Usage
import the CanManager and SensorReading classes
```python
from can_manager import CanManager
from can_manager import SensorReading
```

Instantiate the CanManager class with the channel

```python
bus = CanManager('vcan0')
```
Configure the SensorReadings by calling `bus.read_message_config()` passing the appropriate parameters. This function will read from the `message_config.json` file for the selected project, instantiate a SensorReading object for each reading defined in the configuration, and append to the `self.messages` list contained in the CanManager object.

To send a message on the bus, use the `send_message` method. To read the bus for the latest message, use the `read_bus` method, this will return a `can.Message` object

To assign message data to a SensorReading object, pass a `can.Message` object (Usually the one received from the `read_bus` method) to the `assign_message_data` method, and the method will assign the data to the correct SensorReading object, based off of the can message id.

## Testing
To test the functionality of this class, unless CAN hardware is available, the user must have access to a linux install that contains socketcan, in order to use the virtual can bus (does not seem to work in WSL, not tested in a virtual machine)

- Run `can-sender.py`, this example now contains the correct message configuration for this test case. If the tester wants to see the raw can messages, run `can-receiver.py` to observe output
- Run `can_manager.py`, this will run the test case, which reads `example_message_config.json` file, reads the dts message data, and creates the SensorReading objects. The test then enters an infinite loop, where it reads the latest message on the bus, assigns message data, prints the reading name and data, and then sends a message on the bus containing the hexidecimal representation of the word "control"
