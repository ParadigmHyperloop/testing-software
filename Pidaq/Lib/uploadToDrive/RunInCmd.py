import uploadToDrive 
import os

while 1:
    # Takes the file's path without quotation marks
    CsvPath = input("File Path:")
    # Exits the loop if the path exists
    if os.path.exists(CsvPath):
        break
# prints a list of the folder names available in the json file
print(uploadToDrive.parentDictionary.keys())
folder = input("Folder Name: ")

uploadToDrive.uploadCsv(path, folder)

