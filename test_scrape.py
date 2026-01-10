import requests
from bs4 import BeautifulSoup

def test_scrape():
    url = "https://www.couchbase.com/careers/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("--- H3 Tags (Potential Jobs) ---")
            for h3 in soup.find_all('h3'):
                print(h3.get_text().strip())
            
            print("\n--- Links containing 'careers' or 'jobs' ---")
            for a in soup.find_all('a', href=True):
                if 'greenhouse' in a['href'] or 'jobs' in a['href']:
                    print(f"{a.get_text().strip()} -> {a['href']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_scrape()
