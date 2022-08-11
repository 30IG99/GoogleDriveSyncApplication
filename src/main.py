from __future__ import print_function

import os.path
import re
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
DESTINATION_DRIVE_FOLDER_ID = '1o-zkvL-foz3RgCID6UrHf2OlCMdOv20f'

def main():
    """
    Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    """
    Upload a file to the specified folder and prints file ID, folder ID
    Args: Id of the folder
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        path = input("Folder Location: ")
        dir_list = os.listdir(path) 
        print(f"Start uploading {len(dir_list)} files.")
        for file_item in dir_list:
            print(f"    {file_item}...", end ="")
            file_metadata = {
                'name': file_item,
                'parents': [DESTINATION_DRIVE_FOLDER_ID]
            }
            media = MediaFileUpload(f"{path}/{file_item}",
                                    resumable=True)
            # pylint: disable=maybe-no-member
            file = service.files().create(body=file_metadata, media_body=media,
                                        fields='id').execute()
            print("done")
        print("Finished uploading.")

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')

if __name__ == '__main__':
    main()