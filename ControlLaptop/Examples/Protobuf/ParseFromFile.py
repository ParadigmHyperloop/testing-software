import os
import sys

from resources import Telemetry_pb2

if __name__=="__main__":
    # Get the generated file path
    cwd = os.path.dirname(sys.argv[0])
    filePath = os.path.join(cwd, "generated", "Telem.pb")
    
    # Create a telemetry packet
    telem = Telemetry_pb2.Telemetry()
    
    # Read the file and load the telem packet with the Parsed file contents
    try:
        with open(filePath, "rb") as f:
            content = f.read()
            telem.ParseFromString(content)
    
    # Catch generic exceptions, mostly for catching FileNotFoundError
    except Exception as e:
        print(e)
        
    print(f"PARSED PACKET: \n{telem}")
        
    