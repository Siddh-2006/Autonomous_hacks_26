# API keys, settings
import os
from typing import Optional

class Config:
    # GitHub API
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    
    # News API
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    
    # Other API keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # System settings
    ALERT_THRESHOLD: float = 0.7
    SIGNAL_RETENTION_DAYS: int = 30
    
    # Company to monitor (default)
    DEFAULT_COMPANY: str = "couchbase"