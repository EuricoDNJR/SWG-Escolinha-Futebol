import os
import json
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from .helper import logging
# Define o escopo necessário
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_drive():
    logging.info("Authenticating Google Drive")
    creds = None
    if os.path.exists('token.json'):
        logging.info("Reading token.json")
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def upload_file(file_path, mime_type):
    drive_service = authenticate_drive()
    file_metadata = {'name': os.path.basename(file_path)}
    media = MediaFileUpload(file_path, mimetype=mime_type)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

#Essa função é para baixa para a sua máquina
# def download_file(file_id, destination):
#     drive_service = authenticate_drive()
#     request = drive_service.files().get_media(fileId=file_id)
#     with open(destination, 'wb') as fh:
#         downloader = MediaIoBaseDownload(fh, request)
#         done = False
#         while done is False:
#             status, done = downloader.next_chunk()
#             print("Download %d%%." % int(status.progress() * 100))

def download_file(file_id):
    drive_service = authenticate_drive()
    request = drive_service.files().get_media(fileId=file_id)
    file_stream = io.BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    file_stream.seek(0)
    return file_stream
