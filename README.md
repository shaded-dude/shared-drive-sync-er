# Google Drive Sync

A simple Python program that automatically uploads files from a local folder on your PC to a Google Drive folder that has been shared with you with **Editor** permission.

```text
Your PC
   │
   │  Upload
   ↓
MySharedFolder
   │
   ↓
Google Drive
   │
   ↓
Friend's Shared Folder
```

## Features

*  Automatically uploads new files to Google Drive
*  Automatically updates files when they are modified
*  Supports folders and subfolders
*  Checks for changes every 10 seconds
*  Uses Google OAuth authentication
*  Saves synchronization information locally
*  Does not automatically delete files from Google Drive

---

# Requirements

* Windows 10 / Windows 11
* Python 3.10 or newer
* Google account
* Editor permission to the Google Drive folder

---

# Installation



## 2. Install Required Packages

Open Command Prompt and run:

```bat
py -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Verify the Google package:

```bat
py -c "import google; print('Google package OK')"
```

You should see:

```text
Google package OK
```

---

# Google Cloud Setup

The program uses the Google Drive API to upload files.

## 1. Create a Google Cloud Project

Open Google Cloud Console:

https://console.cloud.google.com/

Create a new project.

Example:

```text
MY DRIVE SYNC
```

---

## 2. Enable Google Drive API

Go to:

```text
APIs & Services
        ↓
Library
        ↓
Google Drive API
```

Click:

```text
Enable
```

---

# OAuth Setup

## 3. Create OAuth Client ID

Go to:

```text
Google Auth Platform
        ↓
Clients
```

Create an OAuth Client.

Select:

```text
Application type: Desktop app
```

Download the credentials JSON file.

Rename it:

```text
credentials.json
```

Place it in the same folder as `sync.py`.

---

# Test User

If your OAuth application is in **Testing** mode, you must add your Google account as a test user.

Go to:

```text
Google Auth Platform
        ↓
Audience
        ↓
Test users
```

Add the Google account that has Editor access to your friend's folder.

For example:

```text
youraccount@gmail.com
```

---

# Project Folder

Your project should look like:

```text
MY DRIVE SYNC/
│
├── sync.py
├── credentials.json
├── token.json
├── sync_database.json
│
└── MySharedFolder/
```

Some files are created automatically the first time the program runs.

### `sync.py`

The main program.

### `credentials.json`

Google OAuth application credentials.

### `token.json`

Stores your Google authorization so you don't have to log in every time.

### `sync_database.json`

Stores information about files that have already been synchronized.

### `MySharedFolder`

The local folder that gets uploaded to Google Drive.

---

# Configure the Google Drive Folder

Open:

```text
sync.py
```

Find:

```python
FOLDER_ID = "PUT_YOUR_FOLDER_ID_HERE"
```

Replace it with the ID of the Google Drive folder your friend shared with you.

For example:

```python
FOLDER_ID = "YOUR_FOLDER_ID"
```

The Folder ID can be found in the folder's URL:

```text
https://drive.google.com/drive/folders/XXXXXXXXXXXX
```

The part after:

```text
/folders/
```

is the Folder ID.

---

# Configure Local Folder

By default, the program uses:

```python
LOCAL_FOLDER = Path("MySharedFolder")
```

This creates:

```text
MY DRIVE SYNC/
└── MySharedFolder/
```

You can also specify another location.

Example:

```python
LOCAL_FOLDER = Path("D:/My Drive Files")
```

---

# Sync Interval

The program checks for changes every 10 seconds by default:

```python
CHECK_INTERVAL = 10
```

To check every 5 seconds:

```python
CHECK_INTERVAL = 5
```

To check every 30 seconds:

```python
CHECK_INTERVAL = 30
```

---

# Running the Program

Open Command Prompt.

Navigate to your project folder:

```bat
cd "C:\Users\YOUR_USERNAME\Documents\MY DRIVE SYNC"
```

Run:

```bat
py sync.py
```

---

# First Run

The first time you run the program, a Google login window will open.

Sign in using the Google account that has Editor access to the shared folder.

After authorization, the program creates:

```text
token.json
```

Future runs should normally use the saved authorization.

---

# Example Output

A normal startup should look like:

```text
============================================================
        shadeddude want to share this with you
============================================================

Authenticating with Google...
Connected to Google Drive.

Remote folder: My Shared Folder
Folder ID: #####

Watching: C:\Users\YOUR_USERNAME\Documents\MY DRIVE SYNC\MySharedFolder
Checking every 10 seconds.

Press Ctrl+C to stop.
```

The real Folder ID is hidden in the terminal and displayed as:

```text
#####
```

---

# Uploading Files

Put a file inside:

```text
MySharedFolder/
```

For example:

```text
MySharedFolder/
└── test.txt
```

The program will detect it and display:

```text
[UPLOAD] test.txt
```

The file will then appear in the Google Drive folder.

---

# Subfolders

Subfolders are supported.

For example:

```text
MySharedFolder/
│
├── test.txt
│
├── Pictures/
│   ├── photo1.jpg
│   └── photo2.jpg
│
└── School/
    └── homework.pdf
```

The program will automatically create the corresponding folders in Google Drive.

Example output:

```text
[UPLOAD] test.txt
[FOLDER CREATED] Pictures
[UPLOAD] Pictures/photo1.jpg
[UPLOAD] Pictures/photo2.jpg
[FOLDER CREATED] School
[UPLOAD] School/homework.pdf
```

---

# Updating Files

If you modify a file that has already been uploaded, the program detects the change.

Example:

```text
[UPDATE] homework.pdf
```

The Google Drive version will be updated.

---

# Important: Current Sync Direction

This version is **one-way**.

```text
PC
 ↓
Google Drive
```

### Supported

| Action               | Result                   |
| -------------------- | ------------------------ |
| Create file on PC    | ✅ Upload                 |
| Modify file on PC    | ✅ Update Drive           |
| Create folder on PC  | ✅ Create Drive folder    |
| Add file to Drive    | ❌ Not downloaded         |
| Modify file in Drive | ❌ Not downloaded         |
| Delete file on PC    | ❌ Not deleted from Drive |
| Delete file on Drive | ❌ Not deleted from PC    |

The program currently only sends files **from your PC to the shared Google Drive folder**.

---

# Safety

The program does **not** automatically delete files from Google Drive.

For example, if you delete:

```text
MySharedFolder/test.txt
```

the Google Drive copy will remain.

This helps prevent accidental deletion of files in a folder that other people may also be using.

---

# Changing OAuth Client ID

If you create a new OAuth Client ID:

1. Download the new credentials JSON.
2. Replace `credentials.json`.
3. Delete `token.json`.
4. Run `sync.py` again.
5. Sign into Google.
6. Authorize the new application.

Do not delete:

```text
sync.py
MySharedFolder/
```

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'google'`

Run:

```bat
py -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Then:

```bat
py sync.py
```

---

## `403: access_denied`

If Google says:

```text
test ยังไม่ผ่านกระบวนการยืนยันตัวตนของ Google
```

your account probably hasn't been added as a test user.

Go to:

```text
Google Auth Platform
        ↓
Audience
        ↓
Test users
```

Add the Google account you are using.

If you previously used another OAuth Client ID, delete:

```text
token.json
```

and run the program again.

---

## `credentials.json was not found`

Make sure the file is in the same folder as `sync.py`:

```text
MY DRIVE SYNC/
├── sync.py
└── credentials.json
```

---

## `Could not access the shared folder`

Check:

* The Folder ID is correct.
* Your Google account has **Editor** permission.
* You are logged into the correct Google account.
* The shared folder still exists.
* Google Drive API is enabled.

---

# Security

Never share these files publicly:

```text
credentials.json
token.json
```

Do not upload them to GitHub or send them to other people.

The Folder ID is not a password, but it is still better not to publicly post it unnecessarily.

---

# Current Limitations

The current version does not support:

* ❌ Google Drive → PC synchronization
* ❌ Automatic deletion synchronization
* ❌ Windows system tray
* ❌ Automatic startup
* ❌ Real-time filesystem monitoring
* ❌ Google Docs/Sheets/Slides synchronization as normal files
* ❌ Multiple Google Drive folders

The program checks the local folder periodically rather than monitoring it continuously.

---



# License

This project is intended for personal use.

Only synchronize files and folders that you have permission to access.
