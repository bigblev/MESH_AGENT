import os
import sys
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from tools.llm_router import chat
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
]

TOKEN_FILE = os.path.expanduser("~/repos/MESH_AGENT/credentials/gmail_token.json")

def get_calendar_service():
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return build('calendar', 'v3', credentials=creds)

def list_events(days=7):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    if not events:
        return "No upcoming events found."
    
    output = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        output.append(f"{start}: {event.get('summary', 'No title')}")
    
    return "\n".join(output)

def meeting_prep(event_title):
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime',
        q=event_title
    ).execute()
    
    events = events_result.get('items', [])
    if not events:
        return f"No upcoming event found matching '{event_title}'"
    
    event = events[0]
    start = event['start'].get('dateTime', event['start'].get('date'))
    attendees = [a.get('email') for a in event.get('attendees', [])]
    description = event.get('description', 'No description')
    
    prompt = f"""Prepare me for this meeting:

Title: {event.get('summary', 'No title')}
Time: {start}
Attendees: {', '.join(attendees) if attendees else 'None listed'}
Description: {description}

Generate:
1. Key talking points
2. Questions to ask
3. What to prepare in advance
4. Desired outcomes"""
    
    return chat(prompt, "strategy")

def daily_agenda():
    service = get_calendar_service()
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    if not events:
        return "No events today."
    
    event_list = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        attendees = [a.get('email') for a in event.get('attendees', [])]
        event_list.append(f"- {start}: {event.get('summary', 'No title')} ({len(attendees)} attendees)")
    
    events_text = "\n".join(event_list)
    prompt = f"""Here is my agenda for today:

{events_text}

Give me a brief daily briefing — what should I focus on, any back-to-back meetings to flag, and how to prioritize my time."""
    
    return chat(prompt, "fast")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calendar_agent.py <list|prep|agenda> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "list":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(list_events(days))
    elif cmd == "prep":
        print(meeting_prep(" ".join(sys.argv[2:])))
    elif cmd == "agenda":
        print(daily_agenda())
