# Investor-Grade CTO Agent - Refined for Executive Thinking
from agents.base_agent import BaseAgent
from data_sources.github_source import GitHubSource
from config import Config
import statistics
from datetime import datetime
import math

class CTOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CTO")
        self.source = GitHubSource()

    def fetch_data(self):
        return self.source.fetch_repo_stats()

    def analyze(self, data):
        """
        Analyze engineering execution health using CTO-grade reasoning.
        Focuses on trends, consistency, and structural risks over raw metrics.
        """
        
        # === 1. EXECUTION VELOCITY ANALYSIS ===
        current = data["commit_velocity_current"]
        prev = data["commit_velocity_prev"]
        
        if prev > 0:
            velocity_change_pct = ((current - prev) / prev) * 100
        else:
            velocity_change_pct = 0.0 if current == 0 else 100.0

        # === 2. CONSISTENCY & VOLATILITY ANALYSIS ===
        # CTOs value predictability over peaks
        repo_commits = list(data["repo_breakdown"].values())
        if repo_commits and len(repo_commits) > 1:
            mean_activity = statistics.mean(repo_commits)
            if mean_activity > 0:
                # Standard deviation / mean = coefficient of variation
                volatility = statistics.stdev(repo_commits) / mean_activity
                # Invert to get consistency (lower volatility = higher consistency)
                consistency_score = max(0.0, 1.0 - volatility)
            else:
                consistency_score = 0.0
        else:
            consistency_score = 1.0 if len(repo_commits) == 1 else 0.0

        # === 3. BUS FACTOR & CONCENTRATION RISK ===
        # Assess organizational health and single-point-of-failure risk
        contributors = data["active_contributors_count"]
        total_commits = sum(repo_commits) if repo_commits else 0
        
        # Concentration risk in repositories
        if repo_commits and total_commits > 0:
            max_repo_commits = max(repo_commits)
            repo_concentration = max_repo_commits / total_commits
            
            # High concentration = high risk
            if repo_concentration > 0.8:
                concentration_risk = "high"
            elif repo_concentration > 0.6:
                concentration_risk = "medium"
            else:
                concentration_risk = "low"
        else:
            concentration_risk = "unknown"

        # === 4. DELIVERY & RELEASE HEALTH ===
        # CTOs trust releases more than commits
        releases = data["recent_releases_count"]
        
        # Release cadence assessment (90-day window)
        if releases == 0:
            release_cadence = "stalled"
            release_health_score = 0.0
        elif releases < 3:  # Less than 1 per month
            release_cadence = "slowing"
            release_health_score = 0.5
        else:
            release_cadence = "normal"
            release_health_score = 1.0

        # === 5. MULTI-DIMENSIONAL HEALTH ASSESSMENT ===
        # No single dimension is decisive alone
        
        # Velocity health
        if velocity_change_pct < -30:
            velocity_health = "declining"
            velocity_score = 0.0
        elif velocity_change_pct < -10:
            velocity_health = "stable"
            velocity_score = 0.5
        else:
            velocity_health = "strong"
            velocity_score = 1.0

        # Contributor health (bus factor assessment)
        if contributors < 3:
            contributor_health = "fragile"
            contributor_score = 0.0
        elif contributors < 6:
            contributor_health = "limited"
            contributor_score = 0.5
        else:
            contributor_health = "healthy"
            contributor_score = 1.0

        # === 6. COMPOSITE EXECUTION HEALTH ===
        # Weight different dimensions based on CTO priorities
        weights = {
            'velocity': 0.35,      # Execution momentum
            'consistency': 0.25,   # Predictability
            'contributors': 0.20,  # Organizational health
            'releases': 0.20       # Delivery capability
        }
        
        composite_score = (
            velocity_score * weights['velocity'] +
            consistency_score * weights['consistency'] +
            contributor_score * weights['contributors'] +
            release_health_score * weights['releases']
        )

        # === 7. SEVERITY & CONFIDENCE CALIBRATION ===
        # Determine overall health and severity
        if composite_score >= 0.7:
            execution_health = "Strong"
            severity = "Low"
        elif composite_score >= 0.4:
            execution_health = "Stable"
            severity = "Medium"
        else:
            execution_health = "Declining"
            severity = "High"

        # Confidence calculation - decreases with volatility and low data volume
        base_confidence = composite_score
        
        # Reduce confidence for high volatility
        volatility_penalty = (1.0 - consistency_score) * 0.3
        
        # Reduce confidence for low data volume
        data_volume_factor = min(1.0, (contributors + total_commits) / 50.0)
        
        confidence = max(0.1, min(1.0, base_confidence - volatility_penalty)) * data_volume_factor

        # === 8. CTO-STYLE EXPLANATION ===
        explanation = self._generate_cto_explanation(
            execution_health, velocity_change_pct, consistency_score,
            contributors, releases, concentration_risk, composite_score
        )

        # === 9. STRUCTURED OUTPUT ===
        return {
            "agent": "CTO",
            "execution_health": execution_health,
            "severity": severity,
            "confidence": round(confidence, 2),
            "signals": {
                "commit_velocity_change_pct": round(velocity_change_pct, 2),
                "active_contributors": contributors,
                "consistency_score": round(consistency_score, 2),
                "release_cadence": release_cadence,
                "core_repo_activity": "high" if total_commits > 50 else "medium" if total_commits > 10 else "low",
                "bus_factor_risk": concentration_risk,
                "composite_health_score": round(composite_score, 2)
            },
            "explanation": explanation,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _generate_cto_explanation(self, health, velocity_change, consistency, 
                                contributors, releases, concentration_risk, composite_score):
        """Generate plain-English CTO-style explanations"""
        
        if health == "Strong":
            explanation = "Engineering execution remains strong, with healthy velocity, consistent contributor activity, and regular releases. "
            
            if velocity_change > 10:
                explanation += f"Velocity has accelerated by {velocity_change:.1f}%, indicating positive momentum. "
            elif velocity_change > 0:
                explanation += f"Velocity is stable with slight growth ({velocity_change:+.1f}%). "
            else:
                explanation += f"Despite minor velocity softening ({velocity_change:.1f}%), overall execution remains robust. "
                
            explanation += f"Team shows healthy diversity with {contributors} active contributors. "
            
            if releases >= 3:
                explanation += f"Release cadence is strong ({releases} releases in 90 days). "
            
            explanation += "No structural execution risk detected."
            
        elif health == "Stable":
            explanation = "Execution is generally stable, though showing some areas of concern. "
            
            if velocity_change < -10:
                explanation += f"Velocity has softened by {abs(velocity_change):.1f}%, which warrants monitoring. "
            else:
                explanation += f"Velocity change ({velocity_change:+.1f}%) appears within normal variance. "
                
            if consistency < 0.5:
                explanation += "Activity patterns show increased volatility, suggesting potential execution inconsistency. "
            
            if contributors < 6:
                explanation += f"Contributor base is somewhat limited ({contributors} active), creating potential bus factor risk. "
            
            if releases < 3:
                explanation += f"Release cadence has slowed ({releases} releases in 90 days). "
                
            explanation += "Situation requires continued monitoring but no immediate action needed."
            
        else:  # Declining
            explanation = "Execution shows signs of decline with multiple concerning signals. "
            
            explanation += f"Velocity has dropped significantly by {abs(velocity_change):.1f}%, indicating structural execution challenges. "
            
            if consistency < 0.3:
                explanation += "High volatility in activity patterns suggests firefighting or unstable execution. "
            
            if contributors < 3:
                explanation += f"Limited contributor base ({contributors} active) creates significant bus factor risk. "
            
            if concentration_risk == "high":
                explanation += "Activity is highly concentrated, increasing single-point-of-failure risk. "
            
            if releases == 0:
                explanation += "No releases in 90 days indicates stalled delivery capability. "
            elif releases < 2:
                explanation += f"Severely reduced release cadence ({releases} releases in 90 days). "
                
            explanation += "This suggests emerging execution risk requiring immediate attention."
        
        return explanation

    def emit_signal(self, result):
        return result