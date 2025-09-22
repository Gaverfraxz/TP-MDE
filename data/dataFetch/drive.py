import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FILE_ID = "1CEUbZyRxXTlI-9CM3GUVPNI_fIKUoBEbXcXy2r-kHl8"

def get_drive_service():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("drive", "v3", credentials=creds)
    return service
  except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f"An error occurred: {error}")

def get_data_file(service, realFileID):
    file_id = realFileID

    # pylint: disable=maybe-no-member
    request = service.files().export_media(fileId=file_id, mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    file = io.BytesIO()
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()
      print(f"Download {int(status.progress() * 100)}.")
    return file.getvalue()



def get_data():
    service = get_drive_service()
    file = get_data_file(service, FILE_ID)
    return file
