import logging
import os
import json
from __future__ import print_function
from datetime import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('credentials.json') 
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

# Searches for the Json file containing folder names and IDS
# These IDs are to be stored manually.
try:
    with open('dictionary.json') as json_file:    
        parentDictionary = json.load(json_file)
except:
    logging.error('Parents dictionary .json file not found')
    exit()
# Change this for the ID of the default folder 
DefaultID = '1VDOOjuOeyNRJgdKmmRTJC1HVjq91F4Q8'

def uploadCsv(filePath, parentName):
    """ Uploads a csv file from a local directory to a folder on Google Drive.

    Parameters:
    "filePath" is the path of the csv file itself and
                should be passed without quotations.
    "parentName" is the name of the testing folder in the drive
            and only a specific set of values are allowed.
    The parent folder is supposedly going to be fixed for a
    long period of time.
    """
    # Searches for the parent name in the dictionary
    for key in parentDictionary.keys():
        if key.lower() == parentName.lower():
            parentKey = key
    try:
        parentFolderID = parentDictionary[parentKey]
    except KeyError:
        # Uploads to a default folder if the folder name does
        # Not exist in the dictionary
        parentFolderID = DefaultID
        logging.error('Folder name not found \nuploading to "Default"')
    
    # Today's date in YYYY-MM-DD format is stored in the variable "date"
    date = datetime.today().strftime('%Y-%m-%d')
    
    # If the folder does not exist, should be the case
    # When running for the first time on a given day
    if checkExistingSubFolder(date, parentFolderID) == 0:
        folder_metadata = {
            'name' : date,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : [parentFolderID]
            }
        # Creates a folder with the given date
        folder = DRIVE.files().create(body = folder_metadata,
                                      fields = 'id').execute()
        # Returns the date folder's ID
        folderId = getFolderId(date, parentFolderID)
    # Executes if the folder already exists  
    elif checkExistingSubFolder(date, parentFolderID) == 1:
        logging.warning("found folder for today's date")
        folderId = getFolderId(date, parentFolderID)
    # Executes if more than one folder exists
    else:
        logging.warning('unexpected count of folders named with a given date')
        return
    
    # Extracts the .csv file name from the path
    filename=os.path.basename(filePath)
    metadata = {'name': filename, 'parents' : [folderId] }
    # Uploads the .csv file
    response = DRIVE.files().create(body=metadata,
                               media_body=filePath).execute()
    
    if response:
        logging.warning('Uploaded "%s" (%s)' % (metadata['name'], response['mimeType']))
    else:
        logging.warning('error in uploading the csv file')
        
def checkExistingSubFolder(folderName, parentFolder):
    """ Queries the drive for the folder with the given name and parent folder
    """
    query = f" name = '{folderName}' and parents = '{parentFolder}'"
    response = DRIVE.files().list(q = query).execute()

    # Returns 0 if no folder exists with today's date
    # In the specified parent folder
    if len(response.get('files',[])) == 0: 
        logging.warning("creating a new folder...")
        return 0
    # Returns 1 if the folder with today's date
    # Exists in the specified parent folder
    elif len(response.get('files',[])) == 1:
            return 1
    else:
        logging.warning("More than one file found")

def getFolderId(fName, parentFolder):
    """ Performs the query to return the ID of the folder with the given name
    """
    # Searches in the drive using the parameters passed
    query = f" name = '{fName}' and parents = '{parentFolder}'"
    response = DRIVE.files().list(q = query).execute()
    # Gets the folder ID of the first and only entry if it exists
    if len(response.get('files',[])) == 1:
        return response.get('files', [])[0].get('id')
