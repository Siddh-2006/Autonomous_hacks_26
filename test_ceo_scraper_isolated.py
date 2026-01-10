import sys
import os

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

from backend.data_sources.news_scraper import fetch_company_news

print("[TEST] Testing CEO Scraper (Live Only)...")
articles = fetch_company_news("Couchbase")
print(f"Articles Found: {len(articles)}")
if articles:
    print("Sample Titles:")
    for a in articles[:3]:
        print(f"- {a['title']}")
else:
    print("Result: EMPTY (RSS Failed)")
