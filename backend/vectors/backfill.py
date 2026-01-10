import sys
import os

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.storage.vector_db import vector_memory
from backend.data_sources.sec_scraper import SECScraper

def run_backfill():
    print("--- STARTING 2-YEAR HISTORICAL BACKFILL ---")
    scraper = SECScraper()
    
    # 1. Fetch History (SEC + Archive)
    # Using the mock method for reliability in this demo environment, 
    # but in prod we would parse the URLs returned by fetch_historical_filings()
    history = scraper.fetch_mock_strategic_history()
    
    print(f"[BACKFILL] Found {len(history)} strategic pillars from 2022-2024.")
    
    # 2. Vectorize and Store
    for item in history:
        print(f"  > Processing: {item['date']} - {item['source']}")
        
        vector_memory.store_narrative(
            agent="CEO_ARCHIVE",
            text=item['text'],
            metadata={
                "timestamp": item['date'], # Backdated
                "source": item['source'],
                "type": "STRATEGIC_BASELINE"
            }
        )
        
    print("--- BACKFILL COMPLETE ---")
    print("The CEO Agent now has a 'Memory' of past promises to check for contradictions.")

if __name__ == "__main__":
    try:
        run_backfill()
    except Exception as e:
        print(f"[ERROR] Backfill failed: {e}")
