from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

CREDENTIALS_FILE = os.path.expanduser("~/repos/MESH_AGENT/credentials/gmail_oauth.json")
TOKEN_FILE = os.path.expanduser("~/repos/MESH_AGENT/credentials/gmail_token.json")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
flow.redirect_uri = 'http://localhost:8085/'

auth_url, _ = flow.authorization_url(
    access_type='offline',
    include_granted_scopes='true',
    prompt='consent'
)

print(f"\nOpen this URL in your browser:\n{auth_url}\n")
print("After authorizing, you will be redirected to localhost:8085")
print("Copy the FULL redirect URL from your browser address bar and paste it here:")
full_url = input("Full redirect URL: ")

from urllib.parse import urlparse, parse_qs
parsed = urlparse(full_url)
code = parse_qs(parsed.query)['code'][0]
flow.fetch_token(code=code)
creds = flow.credentials

with open(TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print("Authentication successful! Token saved.")
