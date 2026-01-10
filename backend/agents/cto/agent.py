from datetime import datetime
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.agents.base_agent import BaseAgent
from backend.data_sources.github_scraper import fetch_github_metrics
from backend.db.database import get_latest_cto_snapshot, insert_cto_snapshot, get_cto_history

class CTOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CTO")

    def analyze(self):
        # 1. Collect Data (Tier 1)
        metrics = fetch_github_metrics("couchbase")
        
        # 2. Intelligence Layer (Analysis)
        current_commits = metrics['total_commits_last_30d']
        prev_commits = metrics['total_commits_prev_30d']
        
        # Avoid division by zero
        if prev_commits > 0:
            velocity_change_pct = ((current_commits - prev_commits) / prev_commits) * 100
        else:
            velocity_change_pct = 0.0 if current_commits == 0 else 100.0
            
        # Decision Logic
        execution_health = "Stable"
        severity = "Low"
        explanation = "Engineering output flows within normal parameters."
        
        # Rule 1: Collapse in Velocity -> Execution Risk
        if velocity_change_pct < -30 and current_commits < 10:
            execution_health = "Declining"
            severity = "High"
            explanation = "CRITICAL: Significant drop in engineering velocity. Commits stalled."
        elif velocity_change_pct < -20:
            execution_health = "Declining"
            severity = "Medium"
            explanation = f"Engineering momentum slowing ({velocity_change_pct:.1f}% drop)."
            
        # Rule 2: Innovation Spike -> Strong Execution
        elif metrics['new_repos_90d'] > 0 and velocity_change_pct > 10:
            execution_health = "Strong"
            severity = "Low"
            explanation = "Innovation detected: New repositories active and commit velocity increasing."
        elif velocity_change_pct > 20:
             execution_health = "Strong"
             severity = "Low"
             explanation = f"Accelerating development velocity ({velocity_change_pct:.1f}% increase)."

        # --- NEW: Bus Factor Analysis (Elite Metric) ---
        # "Bus Factor": If minimal contributors but high commits -> Risk of Knowledge Silo
        contributors = metrics.get('active_contributors', 0)
        if contributors < 3 and current_commits > 50:
             severity = "Medium"
             explanation += " [WARNING: Bus Factor Risk. High output depends on <3 engineers.]"
             # Correlate with 'Tech Debt' - rushing without review?
        
        # 3. Construct Output
        signal = {
            "agent": "CTO",
            "execution_health": execution_health,
            "severity": severity,
            "bus_factor_risk": contributors < 3 and current_commits > 50, # Structured Signal
            "execution_health": execution_health,
            "severity": severity,
            "confidence": 0.9 if metrics['active_contributors'] > 0 else 0.5,
            "signals": {
                "commit_velocity_change_pct": velocity_change_pct,
                "release_cadence": metrics['release_cadence'],
                "new_repos_90d": metrics['new_repos_90d'],
                "active_contributors": metrics['active_contributors']
            },
            "explanation": explanation,
            "timestamp": datetime.now().isoformat(),
            # DB Internal Fields
            "total_commits": current_commits,
            "commit_velocity_change_pct": velocity_change_pct,
            "active_contributors": metrics['active_contributors'],
            "consistency_score": 8.5, # Placeholder for variance calculation
            "release_cadence": metrics['release_cadence'],
            "core_repo_activity": ",".join(metrics['core_repos'][:3])
        }
        
        # 4. Store Snapshot (Tier 3)
        insert_cto_snapshot(signal)
        
        return signal

if __name__ == "__main__":
    agent = CTOAgent()
    result = agent.analyze()
    print(json.dumps(result, indent=2))
