import json

import can

# Function Definitions


def create_can_filters(raw_filters):
    """ Creates a list of can filter objects

    Parameters:
    raw_filters (list): list of message filter objects as defined in the json schema

    Returns:
    can_filters (list): list of python-can filter objects
    """
    can_filters = []
    for raw_can_filter in raw_filters:
        can_id = raw_can_filter["canId"]
        can_mask = raw_can_filter["canMask"]
        extended = raw_can_filter["extended"]
        can_filters.append({
            "can_id": can_id,
            "can_mask": can_mask,
            "extended": extended
        })
    return can_filters


if __name__ == "__main__":
    json_config = open('receiverInfo.json', mode='r')
    can_config = json.load(json_config)
    can_bus = can.Bus(bustype=can_config["canInfo"]["busType"],
                      channel=can_config["canInfo"]["serialPort"],
                      bitrate=can_config["canInfo"]["bitrate"])

    # The can_bus object receives message objects from the sender program
    # Iterating over the bus continuously allows the messages on the bus to be received
    for message in can_bus:
        print(message)
        with open('messages.txt', mode='a+') as message_file:
            message_file.write(f'{message}\r\n')
