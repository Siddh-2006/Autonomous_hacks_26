import sqlite3
import os
import sys
from datetime import datetime, timedelta
import random

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.database import get_db_connection

def seed_executive_history():
    print("--- SEEDING SQLITE HISTORY (INVESTOR TIMELINE) ---")
    conn = get_db_connection()
    c = conn.cursor()
    
    # We want a narrative arc: Stable -> Warning -> Risk (The "Auto-Diligence" Story)
    
    # 1. 6 Months Ago: Stable
    date_1 = (datetime.now() - timedelta(days=180)).isoformat()
    # Schema: timestamp, overall_risk, confidence, summary, supporting_agents
    c.execute('''INSERT INTO executive_snapshots (timestamp, overall_risk, confidence, summary) 
                 VALUES (?, ?, ?, ?)''', 
              (date_1, "Low", 0.9, "Baseline established. Operations stable. Hiring consistently matching growth targets."))

    # 2. 3 Months Ago: Minor Warning
    date_2 = (datetime.now() - timedelta(days=90)).isoformat()
    c.execute('''INSERT INTO executive_snapshots (timestamp, overall_risk, confidence, summary) 
                 VALUES (?, ?, ?, ?)''', 
              (date_2, "Medium", 0.75, "Early warning signal. Minor slowdown in sales hiring detected. Engineering velocity remains high."))
    
    # 3. 1 Month Ago: Strategy Drift
    date_3 = (datetime.now() - timedelta(days=30)).isoformat()
    c.execute('''INSERT INTO executive_snapshots (timestamp, overall_risk, confidence, summary) 
                 VALUES (?, ?, ?, ?)''', 
              (date_3, "Medium", 0.85, "Strategy Drift detected. CEO Narrative shifting towards efficiency. Contradiction with previous growth focus."))

    # 4. Today (Calculated by the live agent elsewhere, but let's ensure we have a 'current' state if missing)
    # We won't insert today's to avoid conflict with live runs, but the history is now populated.

    conn.commit()
    conn.close()
    print("[SUCCESS] Injected 3 historical thesis snapshots into 'executive_snapshots'.")
    print("The Dashboard Timeline will now look populated and trend-aware.")

if __name__ == "__main__":
    seed_executive_history()
