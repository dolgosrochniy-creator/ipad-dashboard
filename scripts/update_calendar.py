import os
import json
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import requests
from icalendar import Calendar
import recurring_ical_events

url = os.environ['ICLOUD_CALENDAR_URL'].replace('webcal://', 'https://', 1)
response = requests.get(url, timeout=30)
response.raise_for_status()
calendar = Calendar.from_ical(response.content)
now = datetime.now(timezone.utc)
end = now + timedelta(days=45)
moscow = ZoneInfo('Europe/Moscow')
events = []

for event in recurring_ical_events.of(calendar).between(now, end):
    start = event.decoded('DTSTART')
    finish = event.decoded('DTEND') if event.get('DTEND') else start
    if isinstance(start, datetime):
        if start.tzinfo is None:
            start = start.replace(tzinfo=moscow)
        if isinstance(finish, datetime) and finish.tzinfo is None:
            finish = finish.replace(tzinfo=moscow)
        start_text = start.isoformat()
        end_text = finish.isoformat() if isinstance(finish, datetime) else str(finish)
    else:
        start_text = start.isoformat()
        end_text = finish.isoformat()
    title = str(event.get('SUMMARY', 'Событие'))
    events.append({'title': title, 'start': start_text, 'end': end_text, 'is_flight': any(x in title.upper() for x in ['HU', 'CA', 'CX', 'SU', 'РЕЙС', 'FLIGHT'])})

events.sort(key=lambda e: e['start'])
with open('calendar_events.json', 'w', encoding='utf-8') as f:
    json.dump({'updated': now.isoformat(), 'events': events}, f, ensure_ascii=False, indent=2)
