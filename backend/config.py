# API keys, settings
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    # GitHub API
    GITHUB_TOKEN: Optional[str] = os.getenv("GITHUB_TOKEN")
    GITHUB_ORG: str = "couchbase"
    
    # Core Repositories (Hardcoded for MVP)
    CORE_REPOS = [
        "couchbase-lite-android",
        "couchbase-lite-ios", 
        "couchbase-net-client",
        "couchbase-java-client",
        "couchbase-python-client"
    ]
    
    # Execution Health Thresholds
    VELOCITY_DROP_DECLINING: float = -30.0  # Percentage drop
    VELOCITY_DROP_STABLE: float = -10.0     # Percentage drop
    
    # Sampling settings
    HISTORY_DAYS: int = 90  # Look back period for velocity calculation
    
    # News API
    NEWS_API_KEY: Optional[str] = os.getenv("NEWS_API_KEY")
    
    # Other API keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # System settings
    ALERT_THRESHOLD: float = 0.7
    SIGNAL_RETENTION_DAYS: int = 30
    
    # Company to monitor (default)
    DEFAULT_COMPANY: str = "couchbase"
    
    # Database
    DB_PATH = os.path.join(os.path.dirname(__file__), "db", "cto_agent.db")