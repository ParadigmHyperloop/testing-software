# Upload CSV files to Google Drive

The script's function is to upload a CSV file containing testing data to the shared Paradigm Google Drive so that it can be accessed by team members.


## Directory contents
1. drive_options.json: A JSON dictionary containing a) the names of the testing folders in the Drive where the CSV files will
be uploaded and b) the ID for each Drive folder.
2. credentials.json: A JSON (file) containing info that the Drive will use to identify under which application or project the files will be uploaded.
3. driveClass.py: The Python script that contains the class implementation responsible for uploading the CSV files to the Drive.
4. runInCmd.py: The Python script that facilitates executing from the command-line interface

## Overview of functionality
**Arguments:** The user provides the path of a csv file and then the name of the testing folder where the file will be uploaded. The user is provided with a list of options for the testing folders to choose from. 

**Organization:**
The script creates a folder with today's date, if one doesn't already exist, in this format
"YYYY-MM-DD" in the chosen testing folder.
For example, all CSV files the user uploads to "wind tunnel" on 2020-06-20 will be in one folder separate from those uploaded to "wind tunnel" on 
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

**Viewing files:** The files will be uploaded in their csv format. In order to open them in the Drive, locate the file you want to open, and double-click on it. Locate "Google Sheets" and choose it.

## Running runInCmd.py from a Raspberry Pi remotely
If this is the first time running, please see "Setting up drive_options.json" and "Getting credentials.json" first.
1. Launch a command-line window
2. Type ```python3 runInCmd.py --noauth_local_webserver```
3. Copy the full path to the CSV file including the file's name and paste it without including quotations.
4. If running for the first time, a link will show up. Copy the link and paste it in your browser. Follow steps 1-3 in Authorization. Otherwise, skip to step 6 below.
5. After you complete the authorization, a code will appear in the browser. Copy the code and paste it in the command line where it says "Enter verification code:". "Authentication Successful" will appear in the command-line.
6. The options for the folders will be displayed. Write the name of the folder where you want the file to be uploaded, and hit enter.
7. The script will tell you whether the upload was successful and if a folder with today's date was created.


## Running runInCmd.py from a laptop or a Raspberry Pi directly
If this is the first time running, please see "Setting up drive_options.json", "Packages", and "Getting credentials.json" first.
1. Open a command-line interface from [Windows](https://www.howtogeek.com/235101/10-ways-to-open-the-command-prompt-in-windows-10/), from [Mac](https://www.wikihow.com/Get-to-the-Command-Line-on-a-Mac), or [Pi](https://www.raspberrypi.org/documentation/usage/terminal/)
2. Type the following: ```Python3 runInCmd.py```
3. Copy the full path to the CSV file including the file's name and paste it without including quotations. [Here](https://www.pcworld.com/article/251406/windows-tips-copy-a-file-path-show-or-hide-extensions.html) is a shortcut to copying it from Windows. If you are running for the first time or if you are directed to a browser tab, please see "Authorization"
4. The options for the folders will be displayed. Write the name of the folder where you want the file to be uploaded, and hit enter. 
5. The script will tell you whether the upload was successful and if a folder with today's date was created.


## Running driveClass.py separately
If this is the first time running, please see "Setting up drive_options.json", "Packages", and "Getting credentials.json" first
1. Stary by import driveClass on the top of the python file
2. create an object of the class then pass the csv file location and the folder in the drive to the execute method.


```
uploadingObj = driveClass.UploadCsv() 

uploadingObj.execute("path/to/your/file.csv", "folder in drive")
```
3. run the file by either ```python3 filename.py``` or ```python3 filename.py --noauth_local_webserver``` based on how you are running the file.

3. The authorization will be the same as when you run the runInCmd.py file, either remotely or on the same device. follow the instructions in one of the previous two sections based on how you are running the file.


## Authorization and first-time use
If running for the first time on any device or if the directory is missing a "client.json" file, the script will open a browser tab prompting the user to grant some permissions. 
1. In the browser, select a Google account. You will see a "this app is not verified" page. Click "advanced", then "go to QuickStart (unsafe)."
2. A pop-up appears requesting the user to grant permissions: "See, edit, create, and delete all of your Google Drive files," click Allow. While the script has no delete commands and just accesses the files under the specified folders,/// it is recommended to run this script on a new Google account made specifically for the testing.
3. After that, you will be asked to confirm your choices for granting the permissions. Click Allow.
4. You should be directed to a blank page that says "The authentication flow has completed." Close the browser tab and return to the command-line. Continue from step 5 in Using runInCmd.py
5. open the driveClass.py file for editing. Change the variable ```defaultID``` under ```__init__(self):``` to the ID of the default folder in the shared drive. The script will upload to "default" if the folder name entered does not match any of the existing folder names in drive_options.

## Setting up drive_options.json
This JSON dictionary drive_options.json will include the names of the testing folders such as "wind tunnel" or "dts" and the corresponding folder IDs in the format { "name1" : "ID1", "name2" : "ID2" }. The names must be all lowercase for the tool to work.

1. In order for the script to locate the folder where it needs to upload the CSV file, the ID must match the corresponding folder's ID in the Drive.
2. To get the folder ID, open Paradigm's Drive, then find the folder where files will be uploaded, for example, "DTS". Open the folder.
3. In the address bar, the URL will be something like "https://drive.google.com/drive/u/1/folders/**1WolqpYfnQDC_T7u7lI45XQLOsl-U71VV**".
4. The folder ID is all the characters after "folders/", highlighted in boldface above. Copy this ID and paste in the drive_options.json as shown below.
5. The name for the folder must be all lowercase. It is highly recommended to make the name the same as the one in the Drive to avoid confusion.

Create a new entry in the JSON file as shown below, where ```testing folder 1``` and ```default``` already exist in drive_options:
```
{

  "default":"1Vnb9UOTatdZUpcBXr1LBjziwNYZzRXQz",

  "testing folder1": "1Kyr_bJ5MSN3b6w1KMZzdJ7YPyTgPxze1",

  "dts": "1WolqpYfnQDC_T7u7lI45XQLOsl-U71VV"

}
```
## Packages
The following packages must be installed for this tool to work. Follow the steps below to install them
1. Launch a command-line window
2. Type ```pip3 install google-api-python-client```. The first package will be installed.
3. Type ```pip3 install oauth2client```. The second package will be installed.

## Getting credentials.json 
1. follow this [link](https://developers.google.com/drive/api/v3/quickstart/python?) and sign in using the dedicated google account. MUN emails would not work.
2. Click the "Enable the Drive API" button. Click Yes then NEXT.
3. Select "Desktop app" then click Create.
4. Download Client Configuration and save it in the same directory with the other files
