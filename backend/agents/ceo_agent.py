# News / narrative
from agents.base_agent import BaseAgent
from data_sources.news import get_news_sentiment

class CEOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CEO")
    
    def fetch_data(self):
        return get_news_sentiment()
    
    def analyze(self, data):
        if data.get("sentiment_score", 0) < 0.3:
            return {"strategic_direction": "Weakening", "severity": "medium"}
        return {"strategic_direction": "Stable"}