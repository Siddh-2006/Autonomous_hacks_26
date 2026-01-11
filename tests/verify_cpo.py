import sys
import os
import unittest

# Fix Path
current = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(current)
if parent not in sys.path:
    sys.path.append(parent)

from backend.agents.cpo.agent import CPOAgent

class TestCPOLive(unittest.TestCase):
    def setUp(self):
        self.agent = CPOAgent()
        print("\n[CPO] Starting Live Product Health Audit...")

    def test_product_audit(self):
        """Verify GitHub Issues & Product Health Logic."""
        result = self.agent.analyze()
        
        # 1. Check Structure
        self.assertEqual(result['agent'], 'CPO')
        self.assertIn(result['product_health'], ['Healthy', 'Stressed', 'Declining'])
        
        # 2. Check Signals
        signals = result['signals']
        print(f"[CPO] Health: {result['product_health']}")
        print(f"[CPO] Open Issues: {signals.get('open_issues', 'N/A')}") # Might be raw metric/logic
        # Wait, agent logic returns 'issue_pressure', raw metrics are in debug keys
        
        print(f"[CPO] Avg Resolution Time: {signals.get('avg_resolution_hours', 0)} hours")
        
        # 3. Validation
        # Couchbase should have some stars
        self.assertGreater(signals.get('total_stars', 0), 100, "CPO found <100 stars. Metric fetch failed?")
        
        # 4. Check DB Storage
        from backend.db.database import get_latest_cpo_snapshot
        snapshot = get_latest_cpo_snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(snapshot['product_health'], result['product_health'])
        print("[CPO] DB Write Confirmed.")

if __name__ == '__main__':
    unittest.main()
