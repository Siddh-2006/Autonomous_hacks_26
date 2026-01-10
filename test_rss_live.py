import requests
import xml.etree.ElementTree as ET

def test_rss():
    url = "https://news.google.com/rss/search?q=Couchbase+strategy&hl=en-US&gl=US&ceid=US:en"
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            # Print first 500 chars to verify XML
            print("Content Preview:", response.text[:500])
            
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            print(f"Found {len(items)} items.")
            if items:
                print("First Item Title:", items[0].find('title').text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rss()
