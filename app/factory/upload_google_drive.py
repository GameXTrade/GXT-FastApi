from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaInMemoryUpload

class GoogleDriveFactory:
    
    def __init__(self):

        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.SERVICE_ACCOUNT_FJSON = "app/factory/service_account.json"
        self.PARENT_FOLDER_ID = "1bwDB5faoIPnDfersI8NmJdzaIWqH_hYl"
        self.credentials = self.authenticate()
    
    def authenticate(self):
        
        credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FJSON, scopes=self.SCOPES
        )
        return credentials
    
    def upload_file(self, fileinstance):
        try:
            service = build('drive', 'v3', credentials=self.credentials)

            file_metadata = {
                'name': fileinstance.filename,
                'parents': [self.PARENT_FOLDER_ID]
            }
        
            media = MediaInMemoryUpload(fileinstance.file.read(), mimetype=fileinstance.content_type)
            uploaded_file = service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
            print(fileinstance.filename, "erfolgreich erstellt")
            return uploaded_file.get("id")
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def share_file(self, file_id):
        try:
            service = build('drive', 'v3', credentials=self.credentials)
            permission = {
                'type': 'anyone',
                'role': 'reader',
            }
            service.permissions().create(
                fileId=file_id,
                body=permission,
            ).execute()

            file = service.files().get(fileId=file_id, fields='webViewLink').execute()
            return file.get('webViewLink')
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None