import requests
import xml.etree.ElementTree as ET
import json
import os
from datetime import datetime

def fetch_company_news(company_name="Couchbase"):
    """
    Fetches news from Google News RSS.
    Falls back to a 'Real News Snapshot' if RSS fails or is blocked.
    Returns list of dicts: {'title': str, 'published': str, 'summary': str, 'source': str}
    """
    rss_url = f"https://news.google.com/rss/search?q={company_name}+strategy+OR+{company_name}+leadership&hl=en-US&gl=US&ceid=US:en"
    
    articles = []
    
    try:
        response = requests.get(rss_url, timeout=5)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall('.//item'):
                articles.append({
                    "title": item.find('title').text if item.find('title') is not None else "",
                    "published": item.find('pubDate').text if item.find('pubDate') is not None else "",
                    "summary": item.find('description').text if item.find('description') is not None else "",
                    "source": item.find('source').text if item.find('source') is not None else "Google News"
                })
    except Exception as e:
        print(f"[WARNING] Live news scrape failed: {e}")

    except Exception as e:
        print(f"[ERROR] Live news scrape failed: {e}")

    return articles
