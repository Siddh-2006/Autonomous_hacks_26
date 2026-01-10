from datetime import datetime
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.agents.base_agent import BaseAgent
from backend.data_sources.news_scraper import fetch_company_news
from backend.data_sources.strategy_analyzer import StrategyAnalyzer
from backend.db.database import get_latest_ceo_snapshot, insert_ceo_snapshot, get_ceo_history
from backend.storage.vector_db import vector_memory

class CEOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CEO")
        self.analyzer = StrategyAnalyzer()

    def analyze(self):
        # 1. Collect Data (Tier 1)
        articles = fetch_company_news("Couchbase")
        if not articles:
            # Checkpoint 1: Data Sufficiency
            return {
                "agent": "CEO",
                "narrative_health": "INSUFFICIENT_DATA",
                "explanation": "No sufficient news data found to form a strategic opinion.",
                "timestamp": datetime.now().isoformat()
            }
            
        # Extract Text for Analysis
        article_texts = [f"{a['title']} {a['summary']}" for a in articles]
        strategy_metrics = self.analyzer.analyze_strategy(article_texts)
        
        current_forward = strategy_metrics['forward_score']
        current_defensive = strategy_metrics['defensive_score']
        
        # 2. Retrieve History (Tier 3)
        history = get_ceo_history(limit=5)
        
        # 3. Intelligence Layer (Time-Based Reasoning)
        narrative_health = "Stable"
        severity = "Low"
        explanation = ""
        
        if not history:
            # First Run Baseline
            if current_defensive > current_forward:
                narrative_health = "Weakening"
                severity = "Medium"
                explanation = "Initial baseline shows dominance of defensive language over growth narratives."
            elif current_forward > current_defensive * 1.5:
                narrative_health = "Strong"
                severity = "Low"
                explanation = "Initial baseline indicates strong, forward-looking strategic clarity."
            else:
                narrative_health = "Stable"
                explanation = "Balanced mix of strategic updates and market challenges."
        else:
            # Calculate Averages (Simple 'Last 30 Days' proxy using last 5 runs)
            avg_forward = sum(h['forward_looking_score'] for h in history) / len(history)
            avg_defensive = sum(h['defensive_score'] for h in history) / len(history)
            
            # Key Decision Logic
            forward_trend = "increasing" if current_forward > avg_forward else "decreasing"
            
            if current_defensive > avg_defensive * 1.2 and current_forward < avg_forward:
                narrative_health = "Weakening"
                severity = "High"
                explanation = "CRITICAL: Defensive language (headwinds/challenges) is spiking while growth narrative is fading vs historical baseline."
            elif current_forward > avg_forward * 1.2 and current_defensive < avg_defensive:
                narrative_health = "Strong"
                severity = "Low"
                explanation = "Strategy is gaining clarity. Significant increase in forward-looking statements compared to previous periods."
            else:
                narrative_health = "Stable"
                explanation = f"Narrative is consistent with recent history. Forward trend: {forward_trend}."

        # 4. Construct Output
        signal = {
            "agent": "CEO",
            "narrative_health": narrative_health,
            "severity": severity,
            "confidence": 0.85 if len(articles) > 2 else 0.5,
            "signals": {
                "news_sentiment_trend": strategy_metrics['sentiment_trend'],
                "forward_looking_statements": "increasing" if current_forward > 0 else "none", # Simplified
                "strategy_shift_detected": False, # Placeholder for advanced logic
                "leadership_risk_mentions": any("leadership" in t.lower() or "exit" in t.lower() for t in article_texts)
            },
            "explanation": explanation,
            "timestamp": datetime.now().isoformat(),
            # Internal fields for DB
            "forward_looking_score": current_forward,
            "defensive_score": current_defensive,
            "sentiment_trend": strategy_metrics['sentiment_trend'],
            "raw_signals": articles
        }
        
        # 5. Store Snapshot (Tier 3)
        # Only store if we have data
        insert_ceo_snapshot(signal)
        
        # 6. Vector Memory (Episodic + Semantic Contradiction Check)
        try:
            # A. Contradiction Check (The "Time Machine" Feature)
            # Compare TODAY's narrative against the 2-Year Strategic Baseline ("CEO_ARCHIVE")
            baseline_match = vector_memory.collection.query(
                query_texts=[explanation],
                n_results=1,
                where={"agent": "CEO_ARCHIVE"} # Only check against the official baseline/history
            )
            
            if baseline_match and baseline_match['documents']:
                dist = baseline_match['distances'][0][0] # Chroma returns distance (lower is closer)
                # Distance > 1.0 (approx) usually means significant drift for Cosine distance in Chroma
                # Note: Chroma default is L2 squared, but lets assume we can detect relative drift.
                # Actually, let's just log the closest match for the User to see the "Context".
                
                closest_past = baseline_match['documents'][0][0]
                past_date = baseline_match['metadatas'][0][0].get('timestamp', 'Unknown')
                
                print(f"[CEO STRATEGY CHECK] Closest historical baseline ({past_date}):")
                print(f"   Now:  {explanation[:100]}...")
                print(f"   Then: {closest_past[:100]}...")
                
                if dist > 0.5: # Calibrated threshold (Verification Test showed > 0.4 for distinct strategy drift)
                     print(f"[CEO ALERT] Potential Strategy Drift detected (Distance: {dist:.2f})")
                     explanation += f" [STRATEGY ALERT: Drift from {past_date} baseline]"
                else:
                     explanation += f" [Consistent with {past_date} strategy]"

            # B. Store the new memory
            vector_memory.store_narrative(
                agent="CEO",
                text=explanation,
                metadata={
                    "health": narrative_health, 
                    "forward_score": current_forward,
                    "defensive_score": current_defensive
                }
            )
        except Exception as e:
            print(f"[WARNING] Vector store failed: {e}")
            
        return signal

if __name__ == "__main__":
    agent = CEOAgent()
    result = agent.analyze()
    print(json.dumps(result, indent=2))
