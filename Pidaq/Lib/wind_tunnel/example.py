from air_properties import linearInterpolation
import os
import logging

logger = logging.getLogger()

while 1:
    filePath = input("CSV File Path, no quotations: ")
    
    # Exits the loop if the path is valid
    if os.path.exists(filePath):
        break
    else:
        logger.warning("Path does not exist. \nPlease enter a valid path: ")

interObject = linearInterpolation(filePath)

value = input("Enter temperature value, or write \"exit\" to end: ")
while(value != "exit"):
    x = interObject.interpolateDensity(value)
    y = interObject.interpolateViscosity(value) 
    print(x) 
    print(y)
    value = input("Enter next temperature value, or write \"exit\" to end: ")