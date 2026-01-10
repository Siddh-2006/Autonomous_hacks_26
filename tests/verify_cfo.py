# Robust Path Add
import sys
import os
current = os.path.dirname(os.path.abspath(__file__))
if current not in sys.path:
    sys.path.append(current)

import unittest

from backend.agents.cfo.agent import CFOAgent

class TestCFOLive(unittest.TestCase):
    def setUp(self):
        self.agent = CFOAgent()
        print("\n[CFO] Starting Live Audit...")

    def test_live_data_fetch(self):
        """Verify Greenhouse API is returning valid job data."""
        result = self.agent.analyze()
        
        # 1. Check Structure
        self.assertIn('agent', result)
        self.assertEqual(result['agent'], 'CFO')
        
        # 2. Check Data Quality
        open_roles = result['signals']['open_roles']
        print(f"[CFO] Open Roles Found: {open_roles}")
        
        # We expect > 0 roles for a live public company
        self.assertGreater(open_roles, 0, "CFO Agent failed to fetch live roles (Count=0). API might be blocked.")
        
        # 3. Check Logic
        self.assertIn(result['financial_mode'], ['Growth', 'Stable', 'Cost-Control'])
        
    def test_snapshot_storage(self):
        """Verify data is hitting the DB."""
        from backend.db.database import get_latest_cfo_snapshot
        snapshot = get_latest_cfo_snapshot()
        self.assertIsNotNone(snapshot)
        print(f"[CFO] DB Check Passed. ID: {snapshot['id']}")

if __name__ == '__main__':
    unittest.main()
