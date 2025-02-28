import os
import requests
import icalendar
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Import user calendar ID from config.py
from config import USER_CALENDAR_ID

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    # Authenticate and return Google Calendar API service
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

def get_skating_events(calendar_id):
    # Retrieve skating events from public calendar
    calendar_url = f'https://calendar.google.com/calendar/ical/{calendar_id}/public/basic.ics'
    response = requests.get(calendar_url)
    response.raise_for_status()
    gcal = icalendar.Calendar.from_ical(response.content)

    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            summary = component.get('SUMMARY')
            if summary and any(keyword in summary.lower() for keyword in ["public skate", "public skating", "adult open skate", "aspire freestyle"]):
                events.append({
                    'summary': summary,
                    'start': component.get('DTSTART').dt,
                    'end': component.get('DTEND').dt
                })
    return events

def insert_event_into_calendar(service, event):
    # Insert event into the user's calendar
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
    service.events().insert(calendarId=USER_CALENDAR_ID, body=event_body).execute()

def event_exists(service, event):
    # Check if event already exists in the user's calendar on the same day
    start_of_day = datetime(event['start'].year, event['start'].month, event['start'].day, 0, 0, 0)
    end_of_day = start_of_day + timedelta(days=1)

    events_result = service.events().list(
        calendarId=USER_CALENDAR_ID,
        timeMin=start_of_day.isoformat() + 'Z',
        timeMax=end_of_day.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    for existing_event in events:
        if 'summary' in existing_event and any(
            keyword in existing_event['summary'].lower() for keyword in 
            ["public skating", "public skate", "adult open skate", "aspire freestyle"]
        ):
            return True
    return False

def main():
    public_skating_calendar_id = "qq3p7mn8h8dtn10dlaphfrkoaam5sh8p@import.calendar.google.com"

    service = authenticate_google_account()
    events = get_skating_events(public_skating_calendar_id)

    for event in events:
        if not event_exists(service, event):
            print(f"Inserting event: {event['summary']}")
            insert_event_into_calendar(service, event)
        else:
            print(f"Event already exists: {event['summary']}")

    print("All events have been processed.")

if __name__ == '__main__':
    main()
