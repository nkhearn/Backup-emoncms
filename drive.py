from __future__ import print_function

import io
import os.path

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_drive_service():
    """Shows basic usage of the Drive v3 API using service account."""

    creds = None
    if os.path.exists('service_account.json'):
        creds = service_account.Credentials.from_service_account_file(
            'service_account.json', scopes=SCOPES)
    else:
        print("service_account.json not found. Please create a service account and download the json key.")
        return None

    try:
        service = build('drive', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def details(service):
    """Lists the drive details, including storage."""
    try:
        drive_about = service.about().get(fields="storageQuota").execute()
        total_space = int(drive_about.get('storageQuota').get('limit'))
        used_space = int(drive_about.get('storageQuota').get('usage'))
        free_space = total_space - used_space

        print(f"Total Space: {total_space / (1024 ** 3):.2f} GB")
        print(f"Used Space: {used_space / (1024 ** 3):.2f} GB")
        print(f"Free Space: {free_space / (1024 ** 3):.2f} GB")
    except Exception as e:
        print(f"An error occurred: {e}")

def plist(service):
    """Lists the names and ids of files and folders in the root of the drive."""
    try:
        results = service.files().list(
            pageSize=1000, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print('Files and folders:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
    except Exception as e:
        print(f"An error occurred: {e}")

def list_files(service, folder_id):
    """Lists the names and ids of files and folders in a folder."""
    try:
        results = service.files().list(
            pageSize=1000, q=f"'{folder_id}' in parents",
            fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            print(f"Files and folders in folder ID {folder_id}:")
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
    except Exception as e:
        print(f"An error occurred: {e}")

def upload_file(service, file_path, file_name, parent_folder_id=None):
    """Uploads a file to the drive."""
    try:
        file_metadata = {'name': file_name}
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]
        media = MediaFileUpload(file_path, resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File ID: {file.get('id')}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_file(service, file_id, file_path):
    """Downloads a file from the drive."""
    try:
        request = service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.", end="\r")

        with open(file_path, 'wb') as f:
            f.write(fh.getvalue())
        print(f"\nFile downloaded to {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    service = get_drive_service()
    if service is None:
        return

    while True:
        print("\nChoose an option:")
        print("1. Details")
        print("2. List root files")
        print("3. List folder files")
        print("4. Upload file")
        print("5. Download file")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            details(service)
        elif choice == '2':
            plist(service)
        elif choice == '3':
            folder_id = input("Enter folder ID: ")
            list_files(service, folder_id)
        elif choice == '4':
            file_path = input("Enter file path: ")
            file_name = input("Enter file name: ")
            parent_folder_id = input("Enter parent folder ID (optional, leave blank for root): ")
            if parent_folder_id:
                upload_file(service, file_path, file_name, parent_folder_id)
            else:
                upload_file(service, file_path, file_name)
        elif choice == '5':
            file_id = input("Enter file ID: ")
            file_path = input("Enter download path: ")
            download_file(service, file_id, file_path)
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
