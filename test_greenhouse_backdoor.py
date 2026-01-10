import requests
import json
import xml.etree.ElementTree as ET

def test_backdoors():
    company_token = "couchbase"
    
    # Target 1: Greenhouse Public API (JSON)
    # Docs: https://developers.greenhouse.io/job-board.html
    api_url = f"https://boards-api.greenhouse.io/v1/boards/{company_token}/jobs?content=true"
    
    print(f"--- Testing API: {api_url} ---")
    try:
        resp = requests.get(api_url, timeout=10)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            jobs = data.get('jobs', [])
            print(f"SUCCESS! Found {len(jobs)} jobs via API.")
            if jobs:
                print(f"Sample: {jobs[0]['title']}")
                return "API"
        else:
            print("API Failed.")
    except Exception as e:
        print(f"API Error: {e}")

    # Target 2: Greenhouse Atom/RSS Feed
    rss_urls = [
        f"https://boards.greenhouse.io/feed/{company_token}",
        f"https://boards.greenhouse.io/{company_token}/rss",
        f"https://boards.greenhouse.io/rss/{company_token}"
    ]
    
    print("\n--- Testing RSS Feeds ---")
    for url in rss_urls:
        print(f"Checking {url}...")
        try:
            resp = requests.get(url, timeout=10)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                # Basic validation it's XML
                if "<feed" in resp.text or "<rss" in resp.text:
                    print("SUCCESS! Found Valid RSS Feed.")
                    return "RSS"
        except Exception as e:
            print(f"RSS Error: {e}")
            
    return None

if __name__ == "__main__":
    result = test_backdoors()
    if result:
        print(f"\n[CONCLUSION] Viable Live Source Found: {result}")
    else:
        print("\n[CONCLUSION] All Backdoors Closed.")
