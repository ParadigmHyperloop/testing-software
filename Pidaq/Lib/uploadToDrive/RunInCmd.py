import driveClass
import logging
import os

while 1:
    # Takes the file's path without quotation marks
    CsvPath = input("File Path:")
    # Exits the loop if the path exists
    if os.path.exists(CsvPath):
        break
    else:
        logging.warning("Path doesnot exist. \n please enter a valid path")
        
uploadingObj = driveClass.UploadCsv()

# prints a list of the folder names available in the json file
print(uploadingObj.parentDictionary.keys())
folder = input("Folder Name: ")

uploadingObj.execute(CsvPath, folder)

