# Google Drive Sync

A simple Python program that automatically syncs files from a local PC folder to a Google Drive folder.

**Current version:** PC → Google Drive

## Requirements

* Windows 10/11
* Python 3.10+
* Google account
* Editor access to the Google Drive folder

## Installation

Install the required packages:

```bash
py -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Project Structure

```text
MY DRIVE SYNC/
├── sync.py
├── credentials.json
├── token.json
├── sync_database.json
└── MySharedFolder/
```

`token.json` and `sync_database.json` are created automatically.

## Google Cloud Setup

1. Create a project in Google Cloud Console.
2. Enable **Google Drive API**.
3. Create an **OAuth Client ID**.
4. Select **Desktop app**.
5. Download the credentials file and rename it to:

```text
credentials.json
```

6. If the OAuth app is in **Testing** mode, add your Google account under **Audience → Test users**.

## Configure Folder

Open `sync.py` and set your Google Drive folder ID:

```python
FOLDER_ID = "YOUR_FOLDER_ID"
```

The Folder ID is the part after `/folders/` in the Google Drive folder URL.

The local folder is:

```python
LOCAL_FOLDER = Path("MySharedFolder")
```

## Run

Open Command Prompt in the project folder:

```bash
py sync.py
```

On the first run, sign in with the Google account that has Editor access.

The program checks for changes every 10 seconds:

```python
CHECK_INTERVAL = 10
```

## How It Works

```text
MySharedFolder
      ↓
Google Drive
```

* New local files → uploaded to Drive
* Modified local files → updated on Drive
* Local folders → created on Drive
* Drive → PC sync is not supported yet
* Files are not automatically deleted from Drive

## Troubleshooting

### `No module named 'google'`

Run:

```bash
py -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### `403: access_denied`

Add your Google account as a **Test user** in:

```text
Google Auth Platform → Audience → Test users
```

If you changed your OAuth Client ID, replace `credentials.json`, delete `token.json`, and run the program again.

## Security

Do not share or upload:

```text
credentials.json
token.json
```
