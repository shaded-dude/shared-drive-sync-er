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

* Automatically uploads new files to Google Drive
* Automatically updates files when they are modified
* Supports folders and subfolders
* Checks for changes every 10 seconds
* Uses Google OAuth authentication
* Saves synchronization information locally
* Does not automatically delete files from Google Drive

---

# Requirements

* Windows 10 / Windows 11
* Python 3.10 or newer
* ofcourse a google account
* Editor permission to the Google Drive folder

---

# Installation



## 1. Install Required Packages

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

# Configure Local Fol
