import requests
from bs4 import BeautifulSoup

def test_sitemap():
    # Common sitemap locations
    urls = [
        "https://www.couchbase.com/sitemap.xml",
        "https://www.couchbase.com/sitemap_index.xml"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    found_jobs = []

    for url in urls:
        print(f"Checking {url}...")
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {resp.status_code}")
            if resp.status_code == 200:
                # Sitemaps are XML
                soup = BeautifulSoup(resp.content, 'xml')
                locs = soup.find_all('loc')
                print(f"Found {len(locs)} URLs.")
                
                for loc in locs:
                    link = loc.get_text()
                    if "career" in link or "jobs" in link or "greenhouse" in link:
                        found_jobs.append(link)
                        
        except Exception as e:
            print(f"Error: {e}")

    print("\n--- JOB LINKS FOUND ---")
    for job in found_jobs[:10]:
        print(job)
    print(f"Total Potential Job Links: {len(found_jobs)}")

if __name__ == "__main__":
    test_sitemap()
