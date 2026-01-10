import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_open_roles():
    """
    Attempts to scrape Couchbase careers.
    Falls back to a real-data snapshot if live scraping fails (common due to 403/JS).
    """
    url = "https://www.couchbase.com/careers/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    roles = []
    
    try:
        # Try Live Fetch
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Attempt to find common job headers (this is heuristic as structure varies)
            for tag in soup.find_all(['h3', 'h4', 'a']):
                text = tag.get_text().strip()
                # Simple heuristic to identify job titles vs menu items
                if len(text) > 4 and ('Engineer' in text or 'Manager' in text or 'Director' in text or 'Sales' in text):
                    roles.append(text)
    except Exception as e:
        print(f"[WARNING] Live scrape failed: {e}")

    # Fallback if live scrape returned nothing (likely due to JS rendering or 403 blocks)
    # NOTE: Couchbase likely uses Greenhouse. A production upgrade would be to hit:
    # https://boards-api.greenhouse.io/v1/boards/{correct_token}/jobs?content=true
    if not roles:
        print("Live scrape returned empty (JS/Auth block). engaging RESILIENCY PROTOCOL -> Using Real Data Snapshot.")
        snapshot_path = os.path.join(os.path.dirname(__file__), 'real_data_snapshot.json')
        if os.path.exists(snapshot_path):
            with open(snapshot_path, 'r') as f:
                data = json.load(f)
                roles = data.get('roles', [])
                print(f"Loaded {len(roles)} roles from snapshot.")

    return roles

def fetch_latest_press_release():
    """
    Fetches latest PR text (Stub for now, uses snapshot).
    """
    snapshot_path = os.path.join(os.path.dirname(__file__), 'real_data_snapshot.json')
    if os.path.exists(snapshot_path):
        with open(snapshot_path, 'r') as f:
            data = json.load(f)
            return data.get('press_release', "")
    return ""
