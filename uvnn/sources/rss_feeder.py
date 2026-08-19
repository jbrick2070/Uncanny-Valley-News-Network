from __future__ import annotations
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import random

DEFAULT_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "http://rss.cnn.com/rss/cnn_topstories.rss"
]

class RSSFeeder:
    def __init__(self, feeds: list[str] = DEFAULT_FEEDS):
        self.feeds = feeds
        self.seen_titles = set()

    def get_random_headline(self) -> str:
        """Fetches a random headline from the configured RSS feeds."""
        feed_url = random.choice(self.feeds)
        try:
            req = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()
                
            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            
            # Find an unseen item
            random.shuffle(items)
            for item in items:
                title = item.find("title")
                desc = item.find("description")
                
                title_text = title.text if title is not None else ""
                desc_text = desc.text if desc is not None else ""
                
                if title_text and title_text not in self.seen_titles:
                    self.seen_titles.add(title_text)
                    return f"News Story: {title_text}. Details: {desc_text}"
                    
        except Exception as e:
            print(f"[RSSFeeder] Failed to fetch {feed_url}: {e}")
            
        return "Local News: A massive sinkhole has swallowed the town hall. Mayor insists it was scheduled."
