# Upload CSV files to Google Drive

The script's function is to upload a CSV file containing testing data to the shared Paradigm Google Drive so that it can be accessed by team members.


## Directory contents
1. drive_options.json: A JSON (library) containing a) the names of the testing folders in the Drive where the CSV files will
be uploaded and b) the ID for each Drive folder.
2. client_secret.json: A JSON (file) containing info that the Drive will use to identify under which (Application or Project) the files will be uploaded.
3. driveClass.py: The Python script that contains the class implementation responsible for uploading the CSV files to the Drive.
4. RunInCmd.py: The Python script that runs in the command-line interface

## Section title
**Arguments:** The user provides the path of a csv file and then the name of the testing folder where the file will be uploaded. The user is provided with a list of options for the testing folders to choose from. The "default" folder option should generally be avoided.

**Organization:**
The script creates a folder with today's date, if one doesn't already exist, in this format
"YYYY-MM-DD" in the corresponding testing folder.
For example, all CSV files the user uploads to "Wind Tunnel" on 2020-06-20 will be in one folder separate from those uploaded to "Wind Tunnel" on 
2020-06-21. Another separate folder will contain CSV files uploaded to "DTS" on 2020-06-20. A folder with the date will be created only if a file was uploaded on a given day. Below is a visualization of how the script will organize the files:
```
Paradigm's Comp5 Google Drive   
│
└───Wind Tunnel
│   │
│   └───2020-06-20
│       │   testingData121.csv
│       │   dataRaw4.csv
│       2020-06-21
│       │   MaxSpeed.csv
│   
└───DTS
│   │
│   └───2020-06-21
│       │   Test2.csv
```

**Viewing files:** The files will be uploaded in their csv format. In order to open them in the Drive, locate the file you want to open, and double-click on it. Under "connected apps", choose "Google Sheets".



## Using RunInCmd.py
1. If this is the first time running, please see "Setting up drive_options.json" and "Getting client_secret.json" first.
2. Open a command-line interface from Windows, [here's how](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/).
3. Type the following: Python RunInCmd.py
4. The script will ask for the complete path for the CSV file. [Here](https://www.pcworld.com/article/251406/windows-tips-copy-a-file-path-show-or-hide-extensions.html) is how to copy it. Paste the path, including the CSV file name, without including quotations. If you are running for the first time or if you are directed to a browser tab, please see "First-time Authorization"
5. The options for the folders will be displayed. Write the name of the folder where you want the file to be uploaded, and hit enter. 
6. The script will tell you whether the upload was successful and if a folder with today's date was created.


## First-time Authorization
If running for the first time on any device or if the directory is missing a "credentials.json" file, the script will open a browser tab prompting the user to grant some permissions. 
1. In the browser, select a Google account. You will see a "this app is not verified" page. Click "advanced", then "go to QuickStart (unsafe)."/// Should we change this name?
2. A pop-up appears requesting the user to grant permissions: "See, edit, create, and delete all of your Google Drive files," click Allow. While the script has no delete commands and just accesses the files under the specified folders,/// it is recommended to run this script on a new Google account made specifically for the testing.
3. After that, you will be asked to confirm your choices for granting the permissions. Click Allow and you should be directed to a blank page that says "The authentication flow has completed." 
4. Close the browser tab and return to the command-line. Continue from step 5 in How to use RunInCmd.py

## Setting up drive_options.json
This JSON (dictionary?) will include the names of the testing folders such as "Wind Tunnel" or "DTS" and the corresponding folder IDs.

The format is { "name" : "ID", "name2" : "ID2" }. In order for the script to locate the folder where it needs to upload the CSV file, the ID must match the corresponding folder's ID in the Drive.

To get the folder ID, open Paradigm's Drive, then find the folder where files will be uploaded, for example, "DTS". Open the folder. In the address bar, the URL will be something like "https://drive.google.com/drive/u/1/folders/1WolqpYfnQDC_T7u7lI45XQLOsl-U71VV".

The folder ID is all the characters after "folders/", in this case, it is "1WolqpYfnQDC_T7u7lI45XQLOsl-U71VV". Copy this ID and paste in the 

drive_options.json. Create a new entry in the JSON file as such, where TestingFolder1/2 already exist in drive_options:
```
{

  "TestingFolder1":"1Vnb9UOTatdZUpcBXr1LBjziwNYZzRXQz",

  "TestingFolder2": "1Kyr_bJ5MSN3b6w1KMZzdJ7YPyTgPxze1",

  "DTS": "1WolqpYfnQDC_T7u7lI45XQLOsl-U71VV"

}
```
## Getting client_secret.json
