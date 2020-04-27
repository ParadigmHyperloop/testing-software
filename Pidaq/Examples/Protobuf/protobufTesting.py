from resources import Telemetry_pb2 
from sys import getsizeof


if __name__=="__main__":
    
    # Create a simple telemtry packet
    message = Telemetry_pb2.Telemetry()
    message.temp = 10
    message.pressure = 5
    message.rpm = 2000
    
    # Get the size
    messageSize = getsizeof(message)

    # Serialize and get new size
    serialized = message.SerializeToString()
    serializedSize = getsizeof(serialized)

    print(f"MESSAGE: \n{message}")
    print(f"SERIALIZED: \n{serialized}\n")
    
    print(f"INITIAL SIZE: {messageSize}")
    print(f"SERIALIZED SIZE: {serializedSize}")
    
