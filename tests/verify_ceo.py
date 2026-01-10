import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.ceo.agent import CEOAgent

class TestCEOLive(unittest.TestCase):
    def setUp(self):
        self.agent = CEOAgent()
        print("\n[CEO] Starting Live Strategy Check...")

    def test_live_news_analysis(self):
        """Verify Google News RSS is live and being analyzed."""
        result = self.agent.analyze()
        
        # 1. Check Data Sufficiency
        if result['narrative_health'] == "INSUFFICIENT_DATA":
             self.fail("CEO Agent found no news articles. RSS feed might be empty or blocked.")
             
        # 2. Check Signals
        signals = result['signals']
        print(f"[CEO] Sentiment: {signals['news_sentiment_trend']}")
        
        # 3. Check Scoring
        self.assertIsInstance(result.get('forward_looking_score'), (int, float))
        self.assertIsInstance(result.get('defensive_score'), (int, float))
        
    def test_db_persistence(self):
         from backend.db.database import get_latest_ceo_snapshot
         snapshot = get_latest_ceo_snapshot()
         self.assertIsNotNone(snapshot)
         print(f"[CEO] DB Check Passed. ID: {snapshot['id']}")

if __name__ == '__main__':
    unittest.main()
