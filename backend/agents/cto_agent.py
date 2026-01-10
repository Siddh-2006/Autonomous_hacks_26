# GitHub / tech health
from agents.base_agent import BaseAgent
from data_sources.github import get_commit_stats

class CTOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CTO")
    
    def fetch_data(self):
        return get_commit_stats("couchbase")
    
    def analyze(self, data):
        if data["commit_change"] < -40:
            return {"tech_health": "declining", "severity": "high"}
        return {"tech_health": "stable"}