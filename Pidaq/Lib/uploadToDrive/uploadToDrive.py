from __future__ import print_function
import os
import logging
from datetime import datetime

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('credentials.json') 
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
    
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))



def uploadCsv(filePath, parent):
    """
    Uploads a csv file from a local directory to a folder on Google Drive.

    Parameters:
    "filePath" is the path of the csv file itself and
                should be passed without quotations.
    "parent" is the name of the testing folder in the drive
            and only a specific set of values are allowed.
    The parent folder is supposedly going to be fixed for a
    long period of time.
    """
    parentDictionary = {'Safety':'1Vnb9UOTatdZUpcBXr1LBjziwNYZzRXQz',
                        'Integrity': '1Kyr_bJ5MSN3b6w1KMZzdJ7YPyTgPxze1',
                        'DTS': '100OsZP0JQIk9_VXHXpK8mdhS9GOp3yKm'}
    parentFolder = parentDictionary[parent]
    #Dictionary for parent folders and their IDs.
    #These IDs are to be stored manually.

    
    date = datetime.today().strftime('%Y-%m-%d')
    #Today's date in YYYY-MM-DD format is stored in the variable "date"
   
    if checkExistingSubFolder(date, parentFolder) == 0:
        #If the folder does not exist, should be the case
        #when running for the first time on a given day
        folder_metadata = {
            'name' : date,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : [parentFolder]
            }
        folder = DRIVE.files().create(body = folder_metadata,
                                      fields = 'id').execute()
        #Creates a folder with the given date
        folderId = getFolderId(date, parentFolder)
        #Returns the date folder's ID
        
    elif checkExistingSubFolder(date, parentFolder) == 1:
        #executes if the folder already exists
        logging.warning("found folder for today's date")
        folderId = getFolderId(date, parentFolder)
    else:
        #executes if more than one folder exists
        logging.warning('unexpected count of folders named with a given date')
        return
    
    fileName=os.path.basename(filePath)
    #extracts the .csv file name from the path
    metadata = {'name': fileName,
                #'mimeType' : 'application/vnd.google-apps.spreadsheet',
                'parents' : [folderId]
                }

    response = DRIVE.files().create(body=metadata,
                               media_body=filePath).execute()
    #uploads the .csv file

    if response:
        logging.warning('Uploaded "%s" (%s)' % (metadata['name'], response['mimeType']))
    else:
        logging.warning('error in uploading the csv file')
        

        
def checkExistingSubFolder(folderName, parentFolder):
    '''
        Queries the drive for the folder with
        the given name and parent folder
    '''
    
    query = " name = '" + folderName + "' and parents = \"" + parentFolder +'"'
    response = DRIVE.files().list(q = query).execute()

    if len(response.get('files',[])) == 0: 
        logging.warning("creating a new folder...")
        return 0
    #Returns 0 if no folder exists with today's date
    #in the specified parent folder
    
    elif len(response.get('files',[])) == 1: 
        for data in response.get('files', []):
            return 1
            #Returns 1 if the folder with today's date
            #exists in the specified parent folder

    else:
        logging.warning("More than one file found")

def getFolderId(fName, parentFolder):
    '''
    Performs the query to return the ID of the folder
    with the given name
    '''
    query = " name = '" + fName + "' and parents = \"" + parentFolder +'"'
    response = DRIVE.files().list(q = query).execute()
    if len(response.get('files',[])) == 1:
        for data in response.get('files', []):
            return data.get('id')
    
