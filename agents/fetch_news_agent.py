import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from utils.db_utils import get_db_connection
from config import RSS_FEEDS

def clean_html(text):
    if not text:
        return ""
    return BeautifulSoup(str(text), "html.parser").get_text(separator=" ").strip()

def fetch_news():
    articles = []
    fetch_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    for category, sources in RSS_FEEDS.items():
        for source, url in sources.items():
            feed = feedparser.parse(url)
            for entry in feed.entries:
                articles.append({
                    "category": category,
                    "source": source,
                    "title": clean_html(entry.get("title")),
                    "link": entry.get("link"),
                    "published": entry.get("published", None),
                    "summary": clean_html(entry.get("summary", "")),
                    "created_at": fetch_time
                })

    conn = get_db_connection()
    cur = conn.cursor()
    for row in articles:
        cur.execute("""
        INSERT OR IGNORE INTO news_today (category, source, title, link, published, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["category"], row["source"], row["title"],
            row["link"], row["published"], row["summary"], row["created_at"]
        ))
    conn.commit()
    conn.close()
    print("✅ News fetched and saved")
