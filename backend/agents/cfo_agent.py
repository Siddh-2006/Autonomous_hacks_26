# Hiring / cost signals
from agents.base_agent import BaseAgent
from data_sources.hiring import get_hiring_stats

class CFOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CFO")
    
    def fetch_data(self):
        return get_hiring_stats()
    
    def analyze(self, data):
        if data.get("hiring_change", 0) < -30:
            return {"financial_mode": "Cost-Control", "severity": "medium"}
        return {"financial_mode": "Growth"}