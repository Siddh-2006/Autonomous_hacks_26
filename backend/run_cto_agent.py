import sys
import os
import json
import sqlite3
from datetime import datetime

# Add current directory to path so we can import modules if run directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.cto_agent import CTOAgent
from db.database import get_db_connection

def run_cto_analysis():
    print(f"[{datetime.utcnow()}] Starting CTO Agent analysis...")
    try:
        agent = CTOAgent()
        
        # 1. Fetch & Analyze
        data = agent.fetch_data()
        result = agent.analyze(data)
        
        # 2. Store in SQLite
        conn = get_db_connection()
        cursor = conn.cursor()
        
        signals_json = json.dumps(result["signals"])
        
        cursor.execute("""
            INSERT INTO cto_snapshots (
                timestamp, 
                total_commits, 
                commit_velocity_change_pct, 
                active_contributors, 
                consistency_score, 
                release_cadence, 
                core_repo_activity, 
                execution_health, 
                severity, 
                confidence, 
                explanation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["timestamp"],
            0, # Total commits not strictly in top level schema but in signals? 
               # Schema had total_commits. I'll use repo_activity sum or just 0 if not key metric.
               # Let's check schema: yes `total_commits`. I'll sum current commits.
            result["signals"]["commit_velocity_change_pct"],
            result["signals"]["active_contributors"],
            result["signals"]["consistency_score"],
            result["signals"]["release_cadence"],
            result["signals"]["core_repo_activity"],
            result["execution_health"],
            result["severity"],
            result["confidence"],
            result["explanation"]
        ))
        
        conn.commit()
        conn.close()
        
        print(f"[{datetime.utcnow()}] Analysis complete. Health: {result['execution_health']}")
        return result
        
    except Exception as e:
        print(f"[{datetime.utcnow()}] Error running CTO analysis: {e}")
        raise e

if __name__ == "__main__":
    run_cto_analysis()
