import json
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

FEEDS = [
    ("Россия", "https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru"),
    ("Мир", "https://news.google.com/rss/headlines/section/topic/WORLD?hl=ru&gl=RU&ceid=RU:ru"),
]
items = []
for category, url in FEEDS:
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=15) as response:
            xml = ET.fromstring(response.read())
        for node in xml.findall("./channel/item")[:6]:
            title = (node.findtext("title") or "").strip()
            link = (node.findtext("link") or "").strip()
            source_node = node.find("source")
            source = (source_node.text or category) if source_node is not None else category
            if title and link:
                items.append({"title": title, "url": link, "source": source, "category": category})
    except Exception as exc:
        print("Feed unavailable:", category, str(exc))
if not items:
    raise SystemExit("No news feeds available; existing file unchanged")
selected = []
for index in range(6):
    for offset in (0, 1):
        group = items[:6] if offset == 0 else items[6:]
        if index < len(group):
            selected.append(group[index])
with open("news_events.json", "w", encoding="utf-8") as out:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "items": selected[:8]}, out, ensure_ascii=False, indent=2)
