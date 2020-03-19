import can
import json

json_config = open('canInfo.json', mode='r')
can_config = json.load(json_config)
can_bus = can.Bus(bustype=can_config["canInfo"]["busType"],
                  channel=can_config["canInfo"]["serialPort"],
                  bitrate=can_config["canInfo"]["bitrate"])

can_messages_raw = [
    message for message in can_config["canInfo"]["messages"]]

can_messages = []
for message_raw in can_messages_raw:
    can_message = {
        "message": can.Message(
            arbitration_id=message_raw["msgId"],
            is_extended_id=message_raw["isExtendedId"],
            data=message_raw["data"]
        ),
        # TODO Change into period (see the python-can documentation)
        "messageFrequency": message_raw["messageFrequency"]
    }
    can_messages.append(can_message)

for can_message in can_messages:
    try:
        can_bus.send_periodic(
            can_message["message"], can_message["messageFrequency"])
        print(f"Message sent on {can_bus.channel_info}")
    except can.CanError:
        print("Error, message not sent")
