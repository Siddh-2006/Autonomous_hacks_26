import sys
import os
import time

# Add root path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.portfolio.manager import get_portfolio
from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent
from backend.alerts.change_detector import ChangeDetector
from backend.alerts.notifier import Notifier
from backend.db.database import get_executive_history, save_executive_verdict, init_db

# Mocking Agent Runs for Demo Speed - or we can run them real?
# For a "cron", we usually assume agents ran recently or we trigger them.
# Given the latency, fine to re-assess based on latest snapshots in DB
# But we need a way to ensure snapshots are fresh.
# For this V1 Cron, let's assume it runs the "Board Assessment" part using whatever data is current,
# OR it runs the whole pipeline. Let's run the Board Assessment (Evaluator).

def run_cron_cycle():
    print(">>> [CRON] Starting Portfolio Scan...")
    portfolio = get_portfolio()
    
    detector = ChangeDetector()
    notifier = Notifier()
    agent = ExecutiveReasoningAgent()
    
    for company in portfolio:
        if not company['active']: continue
        
        print(f"Processing: {company['name']}...")
        
        # 1. Get Previous State (Last 1)
        history = get_executive_history(limit=1)
        prev_verdict = history[0] if history else None
        
        # 2. Run Board Assessment (Fresh Logic on Existing Data)
        # In a full production env, we'd trigger scrapers here too.
        # checking "backend/scheduler/run_agents.py" -> that runs scrapers.
        # We assume scrapers run on their own cadence. This cron checks the *Board*.
        
        curr_verdict = agent.run() # This evaluates current DB state & Adds entry
        # Wait, agent.run() usually saves to DB. 
        # If we save it, then next time it's "previous".
        # We should calculate *before* saving if possible, or just compare N vs N-1.
        
        # The agent.run() saves result. So let's re-fetch history limit=2
        time.sleep(1) # Ensure write
        
        history_new = get_executive_history(limit=2)
        if len(history_new) < 2:
            print("Not enough history for change detection.")
            continue
            
        latest = history_new[0]
        previous = history_new[1]
        
        # 3. Detect Change
        alert = detector.detect_changes(latest, previous)
        
        if alert:
            alert['company'] = company['name']
            print(f"!!! TRIGGER: {alert['reason']}")
            notifier.send_alert(alert)
        else:
            print(f"Status Stable: {latest.get('overall_risk')}")

if __name__ == "__main__":
    init_db() # Ensure DB exists
    run_cron_cycle()
