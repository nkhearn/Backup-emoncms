import os
import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Configuration
SERVICE_ACCOUNT_FILE = 'service_account.json'
UPLOAD_FILE_NAME = 'emoncms-backup-{}.tar.gz' # Filename without the date.
PARENT_FOLDER_ID = None
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_file(file_path, file_name, parent_folder_id=None):
    """Uploads a file to Google Drive using a service account."""
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        print(f"File '{file_name}' uploaded successfully. File ID: {file.get('id')}")

    except Exception as e:
        print(f"An error occurred during upload: {e}")

def main():
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    file_name = UPLOAD_FILE_NAME.format(date_str) # Add the date to the filename.
    file_path = os.path.join("/var/opt/emoncms/backup", file_name)

    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'")
        return

    upload_file(file_path, file_name, PARENT_FOLDER_ID)

if __name__ == "__main__":
    main()
