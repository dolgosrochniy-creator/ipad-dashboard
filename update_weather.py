import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=55.7558&longitude=37.6173"
    "&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m"
    "&hourly=temperature_2m,weather_code"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min"
    "&timezone=Europe%2FMoscow&forecast_days=5"
)

request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urlopen(request, timeout=30) as response:
    data = json.load(response)

data["updated_at"] = datetime.now(timezone.utc).isoformat()

with open("weather_events.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("Moscow weather updated successfully")
