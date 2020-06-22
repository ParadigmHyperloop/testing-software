from __future__ import print_function

import logging
import os
import json
from datetime import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class UploadCsv:
    def __init__(self):   
        
        # Change this for the ID of the default folder 
        self.defaultID = '1VDOOjuOeyNRJgdKmmRTJC1HVjq91F4Q8'
        
        self.SCOPES = 'https://www.googleapis.com/auth/drive'
        self.store = file.Storage('client.json') 
        self.creds = self.store.get()

        if not self.creds or self.creds.invalid:
            self.flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
            self.creds = tools.run_flow(self.flow, self.store)
            
        self.DRIVE = build('drive', 'v3', http= self.creds.authorize(Http()))
            
        # Searches for the Json file containing folder names and IDs
        # These IDs are to be stored manually.
        try:
            with open('drive_options.json') as json_file:
                self.parentDictionary = json.load(json_file)
                
        except FileNotFoundError:
            logging.warning('Json file could not be found, \
            \ncreating a default drive options dictionary file...')
            
            newDictionary = {'default': self.defaultID}
            with open('drive_options.json', 'w') as new_file:    
                json.dump(newDictionary, new_file)
            self.parentDictionary = newDictionary
    
    def execute(self, filePath, parentName):
        """ Uploads a csv file from a local directory to a folder on Google Drive.
        Parameters:
            "filePath" is the path of the csv file itself and
                        should be passed without quotations.
            "parentName" is the name of the testing folder in the drive
                    and only a specific set of values are allowed.
        """
        # Searches for the parent name in the dictionary
        lowerDictionary = {}
        for key, value in self.parentDictionary.items():
            lowerDictionary[key.lower()] = value
        try:
            self.parentFolderID = lowerDictionary[parentName.lower()]
        except KeyError:
            # Uploads to a default folder if the folder name does
            # Not exist in the dictionary
            self.parentFolderID = self.parentDictionary['default']
            logging.warning('Folder name not found \nuploading to "Default"')
                
        # Today's date in YYYY-MM-DD format is stored in the variable "date"
        date = datetime.today().strftime('%Y-%m-%d')
        
        # If the folder does not exist, should be the case
        # When running for the first time on a given day
        if self.__checkExistingSubFolder(date) == 0:
            folder_metadata = {
                'name' : date,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents' : [self.parentFolderID]
                }
            # Creates a folder with the given date
            folder = self.DRIVE.files().create(body = folder_metadata,
                                               fields = 'id').execute()
            # Returns the date folder's ID
            folderId = self.__getFolderId(date)
        # Executes if the folder already exists  
        elif self.__checkExistingSubFolder(date) == 1:
            logging.warning("found folder for today's date")
            folderId = self.__getFolderId(date)
        # Executes if more than one folder exists
        else:
            logging.warning('unexpected count of folders named with a given date')
            return
        
        # Extracts the .csv file name from the path
        filename = os.path.basename(filePath)
        metadata = {'name': filename, 'parents' : [folderId] }
        # Uploads the .csv file
        response = self.DRIVE.files().create(body=metadata,
                                             media_body=filePath).execute()
        
        if response:
            logging.warning('Uploaded "%s" (%s)' % (metadata['name'], response['mimeType']))
        else:
            logging.error('error in uploading the csv file')
        
    def __checkExistingSubFolder(self, folderName):
        """ Queries the drive for the folder with the given name and parent folder"""
        query = f" name = '{folderName}' and parents = '{self.parentFolderID}'"
        response = self.DRIVE.files().list(q = query).execute()

        # Returns 0 if no folder exists with today's date
        # In the specified parent folder
        if len(response.get('files',[])) == 0: 
            logging.warning("creating a new folder with today's date...")
            return 0
        # Returns 1 if the folder with today's date
        # Exists in the specified parent folder
        elif len(response.get('files',[])) == 1:
                return 1
        else:
            logging.warning("More than one file found")

    def __getFolderId(self, fName):
        """ Performs the query to return the ID of the folder with the given name"""
        # Searches in the drive using the parameters passed
        query = f" name = '{fName}' and parents = '{self.parentFolderID}'"
        response = self.DRIVE.files().list(q = query).execute()
        # Gets the folder ID of the first and only entry if it exists
        return response.get('files', [])[0].get('id')   
