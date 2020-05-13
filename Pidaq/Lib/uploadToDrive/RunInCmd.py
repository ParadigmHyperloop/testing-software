import uploadToDrive

path = input("File Path:") #Takes the file's path without quotation marks

while True:
    folder =input("Folder Name (Safety, Integrity, DTS): ")
    if folder == 'Safety' \
       or folder == 'Integrity' \
       or folder == 'DTS':
        break
        

uploadToDrive.uploadCsv(path, folder)

