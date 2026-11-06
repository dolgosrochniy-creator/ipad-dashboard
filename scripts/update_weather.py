import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen

CITIES = [
    ("Moscow", 55.7558, 37.6173, "Europe/Moscow", "weather_events.json"),
    ("Beijing", 39.9042, 116.4074, "Asia/Shanghai", "weather_beijing.json"),
]

for city, lat, lon, tz, filename in CITIES:
    params = {
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m",
        "hourly": "temperature_2m,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum",
        "timezone": tz, "forecast_days": 7,
    }
    url = "https://api.open-meteo.com/v1/forecast?" + urlencode(params)
    try:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(request, timeout=30) as response:
            data = json.load(response)
        if len(data.get("daily", {}).get("time", [])) < 7:
            raise ValueError("Incomplete seven-day forecast")
        data["updated_at"] = datetime.now(timezone.utc).isoformat()
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"{city} seven-day weather updated successfully")
    except Exception as exc:
        print(f"{city} weather update failed; preserving last good file: {exc}")
