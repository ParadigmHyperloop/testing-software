# Courtesy of comp4

import socket
from resources import Telemetry_pb2

# Setup socket

# Localhost IP, generic port
UDP_IP = "127.0.0.1"
UDP_PORT = 5000

# SOCK_DGRAM indicates UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    # Grab raw data from socket
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    
    # Parse proto structure
    telem = Telemetry_pb2.Telemetry()
    telem.ParseFromString(data)
    
    # Print recieved packets details
    print(f"RECIEVED PACKET: {telem}")
