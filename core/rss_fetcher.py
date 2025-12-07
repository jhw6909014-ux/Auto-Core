import feedparser
from typing import List, Dict

def fetch(rss_url: str, max_entries: int = 5) -> List[Dict]:
    feed = feedparser.parse(rss_url)
    results = []
    for entry in feed.entries[:max_entries]:
        eid = getattr(entry, 'id', None) or getattr(entry, 'link', None) or entry.title
        summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
        results.append({
            "id": str(eid),
            "title": entry.title,
            "link": getattr(entry, 'link', ''),
            "summary": summary
        })
    return results
