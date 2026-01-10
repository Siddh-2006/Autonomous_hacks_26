# Legal / governance
from agents.base_agent import BaseAgent

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("RISK")
    
    def fetch_data(self):
        # Placeholder for legal/governance data
        return {"legal_mentions": 0, "exec_exits": 0}
    
    def analyze(self, data):
        if data.get("legal_mentions", 0) > 5:
            return {"risk_type": "Governance", "urgency": "High"}
        return {"risk_type": "None"}