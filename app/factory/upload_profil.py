from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = "app/factory/service_account.json"
PARENT_FOLDER_ID = "1bwDB5faoIPnDfersI8NmJdzaIWqH_hYl"

def authenticate():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return credentials

def upload_basic():
    cred = authenticate()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=cred)

        file_metadata = {
            'name': "image.JPG",
            'parents': [PARENT_FOLDER_ID]  # Make sure to specify the parent folder
        }
        media = MediaFileUpload("app/factory/image.JPG", mimetype="image/jpeg")
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
    
    return file.get("id") if file else None

upload_basic()
