import os
import requests
import icalendar
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    """Authenticate and return the Google Calendar API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def get_public_skating_events(calendar_id):
    """Retrieve public skating events from the public calendar."""
    # Construct the URL for the .ics file from the calendar ID
    calendar_url = f'https://calendar.google.com/calendar/ical/{calendar_id}/public/basic.ics'
    
    response = requests.get(calendar_url)
    response.raise_for_status()
    gcal = icalendar.Calendar.from_ical(response.content)

    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('SUMMARY')
            if summary and "public skating" in summary.lower():
                events.append({
                    'summary': summary,
                    'start': component.get('DTSTART').dt,
                    'end': component.get('DTEND').dt
                })
    return events

def insert_event_into_calendar(service, calendar_id, event):
    """Insert an event into the user's calendar."""
    event_body = {
        'summary': event['summary'],
        'start': {
            'dateTime': event['start'].isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': event['end'].isoformat(),
            'timeZone': 'UTC',
        }
    }
    service.events().insert(calendarId=calendar_id, body=event_body).execute()

def main():
    # Ask the user for inputs
    public_skating_calendar_id = input("Enter the Pegula skating calendar ID: ").strip()
    user_calendar_id = input("Enter your Google Calendar ID: ").strip()

    service = authenticate_google_account()
    events = get_public_skating_events(public_skating_calendar_id)

    for event in events:
        print(f"Inserting event: {event['summary']}")
        insert_event_into_calendar(service, user_calendar_id, event)

    print("All events have been inserted.")

if __name__ == '__main__':
    main()
