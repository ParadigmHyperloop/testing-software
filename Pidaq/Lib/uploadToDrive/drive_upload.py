from __future__ import print_function
import os

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def uploadCsv(filePath):
    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('credentials.json') 
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
        
    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    metadata = {'name': 'testData.csv',
                'mimeType' : 'application/vnd.google-apps.spreadsheet',
                'parents' : ['1CO4KyW5FHYHWAbz2JOh6XeDRzaY9I1WF']
                }

    res = DRIVE.files().create(body=metadata, media_body=filePath).execute()

    if res:
        print('Uploaded "%s" (%s)' % (metadata['name'], res['mimeType']))
