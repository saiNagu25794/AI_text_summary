from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
import json
load_dotenv()

CREDENTIALS_FILE = 'google_credentials.json'

# Scopes for the API you're using (replace as needed)
SCOPES = ['openid', 'email', 'profile']



async def get_redirect_url():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_FILE, SCOPES)  # Create the OAuth2 flow object

    # Generate the authorization URL
    authorization_url,_ = flow.authorization_url()
    return authorization_url
