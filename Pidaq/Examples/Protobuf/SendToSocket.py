# Courtesy of comp4

import os
import sys
import socket

from resources import Telemetry_pb2


def createTelem(packet):
    """ Populate a simple telem proto packet"""
    packet.temp = 10
    packet.pressure = 100
    packet.rpm = 20000

def createGenDir():
    """ If it does not exist, create a dir to hold generated files
    Returns: Absolute path to generated file directory
    """
    cwd = os.path.dirname(sys.argv[0])
    generateDir = os.path.join(cwd, "generated")
    
    if not os.path.exists(generateDir):
        os.mkdir(generateDir)
    
    return generateDir

def main():
    # Create dir to hold generated files
    GEN_DIR = createGenDir()
    
    # Setup socket
    UDP_IP = "127.0.0.1"
    UDP_PORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((UDP_IP, UDP_PORT))
    
    # Generate a packet
    telem = Telemetry_pb2.Telemetry()
    createTelem(telem)
    
    # Send through UDP
    s.send(telem.SerializeToString())
    
    # Write the bytes-like object to a file in /generated
    with open(os.path.join(GEN_DIR, "Telem.pb"), "wb") as output:
        output.write(telem.SerializeToString())
    
    # Write the packet to a txt file in /generated
    with open(os.path.join(GEN_DIR, "Telem.txt"), "+w") as output:
        output.write(f"{telem}")
        
        
if __name__ == "__main__":
    main()