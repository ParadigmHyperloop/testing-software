# Can-sender Program

The `can-sender.py` script and accompanying senderInfo.json file can be used to configure, and send can messages over a Can bus using the canable USB-to-CAN adapter. This program can be used in conjunction with the `can-receiver.py` script to fully send and receive simulated can messages. Instructions for configuring and using the script and its json configuration are as follows:

- Configure a python virtual environment (instructions on wiki), and install the python-can module `pip install python-can` Note: If you are on linux you will also have to install the pyserial module `pip install pyserial`.

- Open the `senderInfo.json` file, and change the serial port to the number assigned to the canable when it is plugged in, adjust the message frequency the correct value in Hz, and add messages to the array as necessary. The program takes the decimal values of the message id and data, and does the conversion to hex.

- Ensure that the canable has the jumpers in the correct configuration, the jumper labelled boot should be on the two pins closest to the wire header, and if the terminating resistor is required, it too should have the jumper on the two pins closest to the wire header.

- In a command prompt/terminal, navigate to the Examples folder, and run `python can-sender.py`, the program should begin to send messages over the can bus, and will print to the console to indicate whether it was sucessful or not

# Can-receiver Program

The `can-receiver.py` script and accompanying receiverInfo.json file can be used to receive can messages over a Can bus using the canable USB-to-CAN adapter. This program can be used in conjunction with the `can-sender.py` script to fully send and receive simulated can messages. Instructions for configuring and using the script and its json configuration are as follows:

- Configure a python virtual environment (instructions on wiki), and install the python-can module `pip install python-can` Note: If you are on linux you will also have to install the pyserial module `pip install pyserial`.

- Open the `receiverInfo.json` file, and change the serial port to the number assigned to the canable when it is plugged in. If required, configure the bus filters using their decimal representation (for more info on how this works, visit <http://www.cse.dmu.ac.uk/~eg/tele/CanbusIDandMask.html>)

- Ensure that the canable has the jumpers in the correct configuration, the jumper labelled boot should be on the two pins closest to the wire header, and if the terminating resistor is required, it too should have the jumper on the two pins closest to the wire header.

- In a command prompt/terminal, navigate to the Examples foler, and run `python can-receiver.py`, the program should begin to receive any messages on the can bus that are within the can filtering, and write their information to a file called `messages.txt`
