# News data source
import requests
from config import Config

def get_news_sentiment():
    """Fetch news sentiment for company"""
    # Placeholder implementation
    # In real implementation, would use News API + sentiment analysis
    return {
        "sentiment_score": 0.25,  # Negative sentiment
        "articles_count": 15,
        "positive_articles": 3,
        "negative_articles": 8,
        "neutral_articles": 4
    }

def get_recent_news(company_name, days=7):
    """Get recent news articles"""
    return {
        "articles": [
            {
                "title": "Company faces challenges",
                "sentiment": "negative",
                "date": "2024-01-09"
            }
        ]
    }