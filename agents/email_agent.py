import os
import sys
import base64
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.llm_router import chat
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels'
]

CREDENTIALS_FILE = os.path.expanduser("~/repos/MESH_AGENT/credentials/gmail_oauth.json")
TOKEN_FILE = os.path.expanduser("~/repos/MESH_AGENT/credentials/gmail_token.json")

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8085, open_browser=False)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_message_body(msg):
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    elif 'body' in msg['payload'] and 'data' in msg['payload']['body']:
        return base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
    return ""

def triage_inbox(max_emails=10):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=max_emails).execute()
    messages = results.get('messages', [])
    
    emails = []
    for msg in messages:
        full_msg = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
        emails.append({
            'from': headers.get('From', ''),
            'subject': headers.get('Subject', ''),
            'date': headers.get('Date', ''),
            'snippet': full_msg.get('snippet', '')
        })

    email_list = "\n\n".join([f"From: {e['from']}\nSubject: {e['subject']}\nDate: {e['date']}\nSnippet: {e['snippet']}" for e in emails])
    
    prompt = f"""Triage these emails for me. For each one:
1. Priority (1-5, where 5 is urgent)
2. Category (Action Required, FYI, Newsletter, Spam)
3. Suggested action

Emails:
{email_list}

Give a concise triage summary."""
    return chat(prompt, "fast")

def summarize_email(subject_search):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q=subject_search, maxResults=1).execute()
    messages = results.get('messages', [])
    if not messages:
        return "No email found matching that search."
    
    full_msg = service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
    headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
    body = get_message_body(full_msg)
    
    prompt = f"""Summarize this email and suggest a reply:

From: {headers.get('From', '')}
Subject: {headers.get('Subject', '')}
Body: {body[:2000]}"""
    return chat(prompt, "fast")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python email_agent.py <triage|summarize> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "triage":
        print(triage_inbox())
    elif cmd == "summarize":
        print(summarize_email(" ".join(sys.argv[2:])))
