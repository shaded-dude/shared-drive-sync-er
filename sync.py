import os
import time
import json
import mimetypes
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


# ============================================================
# GOOGLE DRIVE SYNC
# ============================================================

APP_NAME = "SHADEDSYNC FOR GOOGLE DRIVE"


# CONFIG


# Local folder 
LOCAL_FOLDER = Path("MySharedFolder")

# Shared Folder ID   if u are stupid it is the part after /folder/ 
FOLDER_ID = "1QrZ4CaZZN5ydLWVqGxpIqUITDJ0ZZViT"

# cooldown between each checks
CHECK_INTERVAL = 10

# Google Drive API permissions
SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

# local file 2
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"
DATABASE_FILE = Path("sync_database.json")


# GOOGLE AUTHENTICATION

def authenticate():
    """Authenticate the user with Google."""

    credentials = None

    # Load existing login
    if os.path.exists(TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not credentials or not credentials.valid:

        if (
            credentials
            and credentials.expired
            and credentials.refresh_token
        ):
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(
                port=0
            )

        with open(
            TOKEN_FILE,
            "w",
            encoding="utf-8"
        ) as token:
            token.write(credentials.to_json())

    return build(
        "drive",
        "v3",
        credentials=credentials
    )


# LOCAL DATABASE


def load_database():
    """Load the local sync database."""

    if not DATABASE_FILE.exists():
        return {}

    try:
        with open(
            DATABASE_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_database(database):
    """Save the local sync database."""

    with open(
        DATABASE_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            database,
            file,
            indent=2,
            ensure_ascii=False
        )


# GOOGLE DRIVE FUNCTIONS

def find_drive_file(service, name, parent_id):
    """Find a file/folder inside a specific Google Drive folder."""

    safe_name = name.replace("\\", "\\\\").replace("'", "\\'")

    query = (
        f"name = '{safe_name}' "
        f"and '{parent_id}' in parents "
        f"and trashed = false"
    )

    result = service.files().list(
        q=query,
        spaces="drive",
        fields=(
            "files("
            "id,"
            "name,"
            "size,"
            "modifiedTime,"
            "md5Checksum,"
            "mimeType"
            ")"
        )
    ).execute()

    files = result.get("files", [])

    if files:
        return files[0]

    return None


def create_drive_folder(service, name, parent_id):
    """Create a folder in Google Drive."""

    metadata = {
        "name": name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id]
    }

    folder = service.files().create(
        body=metadata,
        fields="id,name"
    ).execute()

    print(f"[FOLDER CREATED] {name}")

    return folder["id"]


def get_or_create_folder(service, name, parent_id):
    """Find a folder or create it if it doesn't exist."""

    existing = find_drive_file(
        service,
        name,
        parent_id
    )

    if existing:

        if (
            existing["mimeType"]
            == "application/vnd.google-apps.folder"
        ):
            return existing["id"]

        raise Exception(
            f"A file already exists with the name: {name}"
        )

    return create_drive_folder(
        service,
        name,
        parent_id
    )

# FILE UPLOAD


def upload_file(
    service,
    local_path,
    parent_id,
    database,
    relative_path
):
    """Upload or update a file on Google Drive."""

    filename = local_path.name

    existing = find_drive_file(
        service,
        filename,
        parent_id
    )

    mime_type, _ = mimetypes.guess_type(
        str(local_path)
    )

    if mime_type is None:
        mime_type = "application/octet-stream"

    media = MediaFileUpload(
        str(local_path),
        mimetype=mime_type,
        resumable=True
    )

    # UPDATE EXISTING FILE


    if existing:

        print(f"[UPDATE] {relative_path}")

        service.files().update(
            fileId=existing["id"],
            media_body=media
        ).execute()

        file_id = existing["id"]

    # UPLOAD NEW FILE
   

    else:

        print(f"[UPLOAD] {relative_path}")

        metadata = {
            "name": filename,
            "parents": [parent_id]
        }

        uploaded = service.files().create(
            body=metadata,
            media_body=media,
            fields="id,name"
        ).execute()

        file_id = uploaded["id"]

    # Save file information
    database[str(relative_path)] = {
        "id": file_id,
        "size": local_path.stat().st_size,
        "modified": local_path.stat().st_mtime
    }

# DIRECTORY SYNCHRONIZATION

def sync_directory(
    service,
    local_directory,
    drive_parent_id,
    database,
    relative_directory=Path("")
):
    """Synchronize a local directory with Google Drive."""

    try:
        items = local_directory.iterdir()

    except OSError as error:
        print(
            f"[ERROR] Cannot read folder: "
            f"{local_directory}"
        )
        print(error)
        return

    for item in items:

        relative_path = (
            relative_directory / item.name
        )

     
        # DIRECTORY
       

        if item.is_dir():

            drive_folder_id = get_or_create_folder(
                service,
                item.name,
                drive_parent_id
            )

            sync_directory(
                service,
                item,
                drive_folder_id,
                database,
                relative_path
            )

       
        # FILE
        

        elif item.is_file():

            try:
                stat = item.stat()

            except OSError:
                continue

            old_data = database.get(
                str(relative_path)
            )

            changed = True

            if old_data:

                same_size = (
                    old_data.get("size")
                    == stat.st_size
                )

                same_modified = (
                    old_data.get("modified")
                    == stat.st_mtime
                )

                if same_size and same_modified:
                    changed = False

            if changed:

                upload_file(
                    service,
                    item,
                    drive_parent_id,
                    database,
                    relative_path
                )



# CONNECTION TEST


def check_drive_folder(service):
    """Check whether the configured folder is accessible."""

    try:

        folder = service.files().get(
            fileId=FOLDER_ID,
            fields="id,name,mimeType,capabilities"
        ).execute()

        if (
            folder["mimeType"]
            != "application/vnd.google-apps.folder"
        ):
            print(
                "[ERROR] The configured ID is not a folder."
            )
            return None

        return folder

    except HttpError as error:

        print()
        print("[ERROR] Cannot access the Google Drive folder.")
        print()
        print("Possible reasons:")
        print("  • The folder was deleted")
        print("  • Your Google account lost access")
        print("  • You are logged into the wrong account")
        print("  • The Folder ID is incorrect")
        print()
        print(f"Google error: {error}")
        return None



# MAIN 


def main():

    print()
    print("=" * 60)
    print("              I SYNC SHARE FOLDER 3000")
    print("=" * 60)
    print()


    if FOLDER_ID == "PUT_YOUR_FOLDER_ID_HERE":

        print("[ERROR] FOLDER_ID has not been configured.")
        print()
        input("Press Enter to exit...")
        return

    if not os.path.exists(CREDENTIALS_FILE):

        print(
            f"[ERROR] {CREDENTIALS_FILE} was not found."
        )

        print()
        print(
            "Put your Google OAuth credentials file "
            "in the same folder as sync.py."
        )

        print()
        input("Press Enter to exit...")
        return


    LOCAL_FOLDER.mkdir(
        exist_ok=True
    )


    print("Authenticating with Google...")

    try:

        service = authenticate()

    except Exception as error:

        print()
        print("[ERROR] Authentication failed.")
        print()
        print(error)

        print()
        input("Press Enter to exit...")
        return

    print("Connected to Google Drive.")
    print()


    folder = check_drive_folder(
        service
    )

    if folder is None:

        input("Press Enter to exit...")
        return

    print(
        f"Remote folder: {folder['name']}"
    )

    print(
        "Folder ID: #############################"
    )

    print()


    database = load_database()

    print(
        f"Watching: {LOCAL_FOLDER.absolute()}"
    )

    print(
        f"Checking every {CHECK_INTERVAL} seconds."
    )

    print()
    print("PC  --->  Google Drive")
    print()
    print("Press Ctrl+C to stop.")
    print()


    try:

        while True:

            try:

                sync_directory(
                    service,
                    LOCAL_FOLDER,
                    FOLDER_ID,
                    database
                )

                save_database(database)

            except HttpError as error:

                print()
                print("[GOOGLE DRIVE ERROR]")
                print(error)
                print()

            except Exception as error:

                print()
                print("[SYNC ERROR]")
                print(error)
                print()

            time.sleep(
                CHECK_INTERVAL
            )

    except KeyboardInterrupt:

        print()
        print()
        print("Sync stopped.")
        print("Goodbye!")


if __name__ == "__main__":
    main()