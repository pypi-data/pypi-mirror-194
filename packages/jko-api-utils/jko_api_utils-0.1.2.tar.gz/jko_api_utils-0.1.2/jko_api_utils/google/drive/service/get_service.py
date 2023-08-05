
import io
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def get_service(client_secret_file_path, scopes, token_file_path=None):
    # Load or create credentials for the Google Drive API

    # Assumes that the client secret file is in the same directory as the token file
    if token_file_path is None:
        token_file_path = os.path.join(os.path.dirname(
            client_secret_file_path), 'token.json')

    creds = None
    if os.path.exists(token_file_path):
        creds = Credentials.from_authorized_user_file(token_file_path, scopes)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file_path, scopes)
        creds = flow.run_local_server(port=0)
        with open(token_file_path, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def get_service_with_service_or_secret_path(service, client_secret):
    # Give the user the option to provide the service or the path to the client secret
    if service is None and client_secret is None:
        raise ValueError(
            "Either client_secret or service must be specified.")
    elif service is None:
        service = get_service(
            client_secret, ['https://www.googleapis.com/auth/drive.readonly'])
    return service
