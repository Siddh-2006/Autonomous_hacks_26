# Simple JSON registry for V1
# In a real app, this would be a SQL Table
import json
import os

PORTFOLIO_FILE = os.path.join(os.path.dirname(__file__), 'companies.json')

DEFAULT_PORTFOLIO = [
    {
        "id": "couchbase",
        "name": "Couchbase",
        "github_org": "couchbase",
        "ticker": "BASE",
        "greenhouse_board": "couchbase",
        "active": True
    }
]

def get_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'w') as f:
            json.dump(DEFAULT_PORTFOLIO, f, indent=2)
            return DEFAULT_PORTFOLIO
    
    with open(PORTFOLIO_FILE, 'r') as f:
        return json.load(f)
