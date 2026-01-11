from datetime import datetime
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.agents.base_agent import BaseAgent
from backend.data_sources.github_scraper import fetch_github_metrics
from backend.db.database import insert_cpo_snapshot, get_latest_cpo_snapshot

class CPOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CPO")

    def analyze(self):
        # 1. Collect Data (Tier 1)
        # We assume the "Product" is the same as the "Repo" for this MVP.
        # In V2, we might map Product -> Multiple Repos.
        metrics = fetch_github_metrics("couchbase")
        
        # 2. Intelligence Layer (The CPO Brain)
        
        # A. Dimension: Adoption Momentum (Proxy: Stars & Forks)
        # In a real run, we would compare vs DB history.
        # For MVP, we look at fork_count (high forks = developers building ON it).
        adoption_trend = "flat"
        if metrics.get('new_repos_90d', 0) > 2: # Proxy for ecosystem growth
            adoption_trend = "up"
        
        # B. Dimension: User Pain (Issue Pressure)
        # Pressure = Open / Closed ratio. 
        # If 100 open and 10 closed in 30d -> High Pressure.
        open_issues = metrics.get('open_issues', 0)
        closed_30d = metrics.get('closed_issues_30d', 0)
        
        issue_pressure = "low"
        if closed_30d > 0:
            ratio = open_issues / closed_30d
            if ratio > 20: issue_pressure = "high"
            elif ratio > 10: issue_pressure = "medium"
        elif open_issues > 50:
            issue_pressure = "high" # Infinite backlog

        # C. Dimension: Responsiveness (Time to Resolution)
        avg_res_time = metrics.get('avg_resolution_time_hours', 0)
        responsiveness = "normal"
        if avg_res_time < 24:
            responsiveness = "fast"
        elif avg_res_time > 168: # 1 Week
            responsiveness = "slow"
            
        # D. Ecosystem Dependency (Proxy: Forks & Contributors)
        ecosystem = "moderate"
        if metrics.get('total_forks', 0) > 1000:
            ecosystem = "strong"
        elif metrics.get('total_forks', 0) < 50:
            ecosystem = "weak"

        # 3. Decision Logic (State Machine)
        product_health = "Healthy"
        severity = "Low"
        explanation = "Product shows balanced adoption and maintenance."
        confidence = 0.8
        
        # Rule 1: The "Death Spiral" (Declining)
        # Slow response + High Pressure
        if responsiveness == "slow" and issue_pressure == "high":
            product_health = "Declining"
            severity = "High"
            explanation = "CRITICAL: Maintenance collapse. Valid user issues are piling up with slow resolution (>1 week)."
            confidence = 0.95
            
        # Rule 2: Growing Pains (Stressed)
        # High Pressure BUT Fast Response (They are trying)
        elif issue_pressure == "high" and responsiveness == "fast":
            product_health = "Stressed"
            severity = "Medium"
            explanation = "Scaling Stress: User demand (issues) is outpacing the team, but maintainers are responsive."
            confidence = 0.9

        # Rule 3: Zombie Product (Declining)
        # Weak Ecosystem + Low Activity
        elif ecosystem == "weak" and metrics.get('total_commits_last_30d', 0) < 2:
            product_health = "Declining"
            severity = "Medium"
            explanation = "Stagnation: Low ecosystem interest and minimal maintenance activity."

        # Rule 4: Healthy Growth
        elif adoption_trend == "up" and responsiveness != "slow":
            product_health = "Healthy"
            severity = "Low"
            explanation = "Strong Signals: Ecosystem is growing and team is keeping up with issues."

        # 4. Construct Signal
        signal = {
            "agent": "CPO",
            "product_health": product_health,
            "severity": severity,
            "confidence": confidence,
            "signals": {
                "adoption_trend": adoption_trend,
                "issue_pressure": issue_pressure,
                "maintainer_responsiveness": responsiveness,
                "ecosystem_dependency": ecosystem,
                # Raw data for debugging
                "total_stars": metrics.get('total_stars'),
                "avg_resolution_hours": float(f"{avg_res_time:.1f}")
            },
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        
        # 5. Store Snapshot
        insert_cpo_snapshot(signal)
        
        return signal

if __name__ == "__main__":
    agent = CPOAgent()
    print(json.dumps(agent.analyze(), indent=2))
