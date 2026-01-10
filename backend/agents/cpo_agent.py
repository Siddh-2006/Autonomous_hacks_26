# Product signals
from agents.base_agent import BaseAgent
from data_sources.product import get_product_signals
from typing import Dict, Any

class CPOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CPO")
    
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch product-related data"""
        return get_product_signals()
    
    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze product health and user sentiment"""
        if not data:
            return {"product_signal": "unknown", "reason": "No data available"}
        
        release_frequency = data.get("release_frequency", 0)
        user_complaints = data.get("user_complaints", 0)
        feature_requests = data.get("feature_requests", 0)
        
        if user_complaints > 10 and release_frequency < 2:
            return {
                "product_signal": "Negative Drift",
                "reason": "Feature stagnation, repeated complaints"
            }
        elif release_frequency > 5 and user_complaints < 3:
            return {
                "product_signal": "Positive Momentum",
                "reason": "Regular releases, low complaint volume"
            }
        else:
            return {
                "product_signal": "Stable",
                "reason": "Normal product development pace"
            }