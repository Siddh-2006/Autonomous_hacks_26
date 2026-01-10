# GitHub / tech health
from agents.base_agent import BaseAgent
from data_sources.github_source import GitHubSource
from config import Config
import statistics
from datetime import datetime

class CTOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CTO")
        self.source = GitHubSource()

    def fetch_data(self):
        return self.source.fetch_repo_stats()

    def analyze(self, data):
        # 1. Calculate Velocity Change
        current = data["commit_velocity_current"]
        prev = data["commit_velocity_prev"]
        
        if prev > 0:
            velocity_change_pct = ((current - prev) / prev) * 100
        else:
            velocity_change_pct = 0.0 if current == 0 else 100.0

        # 2. Determine Execution Health & Severity
        health = "Strong"
        severity = "Low"
        
        if velocity_change_pct < Config.VELOCITY_DROP_DECLINING: # < -30%
            health = "Declining"
            severity = "High"
        elif velocity_change_pct < Config.VELOCITY_DROP_STABLE: # < -10%
            health = "Stable"
            severity = "Medium"
        else:
            health = "Strong"
            severity = "Low"

        # 3. Calculate Confidence
        # confidence = 1 - abs(commit_velocity_change_pct) / 100
        # Clamped at 0
        confidence = max(0.0, 1.0 - (abs(velocity_change_pct) / 100.0))

        # 4. Consistency Score (Proxy: Standard deviation of core repo activity? Or bus factor?)
        # For MVP, we'll use a simple spread of activity across repos as consistency
        repo_commits = list(data["repo_breakdown"].values())
        if repo_commits:
            consistency_score = 1.0 - (statistics.stdev(repo_commits) / (statistics.mean(repo_commits) + 1))
            consistency_score = max(0.0, consistency_score)
        else:
            consistency_score = 0.0

        # 5. Core Repo Activity
        # Check if activity is dominated by one repo
        # logic: if max_repo_commits > 80% of total
        core_activity_status = "high"
        if data["commit_velocity_current"] < 10:
            core_activity_status = "low"
        
        # 6. Release Cadence
        releases = data["recent_releases_count"]
        # 3 months period. 0 releases = stalled?
        if releases == 0:
            cadence = "stalled"
        elif releases < 3: # Less than 1 per month
            cadence = "slowing"
        else:
            cadence = "normal"

        # 7. Explanation
        explanation = f"Engineering execution is {health}. "
        if health == "Declining":
            explanation += f"Velocity dropped by {abs(velocity_change_pct):.1f}% over the last quarter. "
        elif health == "Stable":
            explanation += f"Velocity is slighty down ({abs(velocity_change_pct):.1f}%) but within normal variance. "
        else:
            explanation += f"Velocity is strong ({velocity_change_pct:+.1f}%). "
        
        explanation += f"Active contributors: {data['active_contributors_count']}. "
        explanation += f"Release cadence is {cadence} ({releases} releases in 90 days)."

        return {
            "agent": "CTO",
            "execution_health": health,
            "severity": severity,
            "confidence": round(confidence, 2),
            "signals": {
                "commit_velocity_change_pct": round(velocity_change_pct, 2),
                "active_contributors": data["active_contributors_count"],
                "consistency_score": round(consistency_score, 2),
                "release_cadence": cadence,
                "core_repo_activity": core_activity_status
            },
            "explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def emit_signal(self, result):
        return result