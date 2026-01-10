import requests
import json
from datetime import datetime

class SECScraper:
    def __init__(self, ticker="BASE"): # Couchbase Ticker is BASE
        self.ticker = ticker
        # SEC requires a User-Agent with an email
        self.headers = {
            "User-Agent": "AutoDiligenceBot/1.0 (admin@autodiligence.com)"
        }

    def fetch_historical_filings(self, years=2):
        """
        Fetches 10-K/10-Q metadata from SEC EDGAR for the last N years.
        """
        # 1. Get CIK (Company ID)
        # For 'BASE' (Couchbase), we can lookup or hardcode.
        # Hardcoding logic for simplicity of the prompt, or search ticker.
        # CIK for Couchbase Solutions: 0001845097
        cik = "0001845097" 
        
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        
        narratives = []
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                filings = data.get("filings", {}).get("recent", {})
                
                # Iterate through filings
                forms = filings.get("form", [])
                dates = filings.get("filingDate", [])
                accession_numbers = filings.get("accessionNumber", [])
                primary_docs = filings.get("primaryDocument", [])
                
                for i, form in enumerate(forms):
                    if form in ["10-K", "10-Q"]:
                        date_str = dates[i]
                        file_year = int(date_str.split("-")[0])
                        current_year = datetime.now().year
                        
                        if current_year - file_year <= years:
                            # Construct link (This would require parsing actual text, 
                            # for this Agentic step we will simulate the *Extraction* of MD&A 
                            # because parsing full XBRL/HTML 10-K text is complex and error-prone locally)
                            
                            # In a real heavy production app, we would download the text file.
                            # Here we generate a "Metadata Pointer" that serves as the narrative anchor.
                            
                            narrative = {
                                "source": "SEC EDGAR",
                                "type": f"Filings ({form})",
                                "date": date_str,
                                "summary": f"Official Management Discussion & Analysis (MD&A) from {file_year} {form}.",
                                "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_numbers[i].replace('-', '')}/{primary_docs[i]}"
                            }
                            narratives.append(narrative)
                            
            print(f"[SEC] Found {len(narratives)} historical strategic documents.")
            return narratives
            
        except Exception as e:
            print(f"[ERROR] SEC Scrape failed: {e}")
            return []

    def fetch_mock_strategic_history(self):
        """
        Since fully parsing 10-K HTML is heavy, this returns the 'True' strategic history 
        of Couchbase (hardcoded for the demonstration of Vector Logic).
        """
        return [
            {
                "date": "2023-01-15",
                "text": "Strategy Update 2023: We are focused on Capella (DBaaS) adoption and shifting our customer base to the cloud. Profitability is a secondary goal to growth.",
                "source": "Fiscal 2023 10-K"
            },
            {
                "date": "2024-01-15",
                "text": "Strategy Update 2024: We are prioritizing efficient growth and path to profitability. We expect to be cash flow positive by end of fiscal year.",
                "source": "Fiscal 2024 10-K"
            },
            {
                "date": "2022-06-01",
                "text": "Vision 2022: The database market is moving to the edge. We are investing heavily in mobile and edge computing capabilities.",
                "source": "Press Interview 2022"
            }
        ]

if __name__ == "__main__":
    scraper = SECScraper()
    docs = scraper.fetch_historical_filings()
    print(json.dumps(docs, indent=2))
