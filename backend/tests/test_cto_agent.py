import unittest
import sys
import os
import json
from unittest.mock import MagicMock, patch

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__))))

from agents.cto_agent import CTOAgent
from config import Config

class TestCTOAgent(unittest.TestCase):
    def setUp(self):
        try:
            self.agent = CTOAgent()
        except Exception as e:
            print(f"SETUP FAILED: {e}")
            raise e
        
    def test_analyze_declining_health(self):
        """Test that >30% drop triggers Declining/High severity"""
        # Mock data: Current dropped by 40% compared to Prev
        data = {
            "commit_velocity_current": 60,
            "commit_velocity_prev": 100,
            "active_contributors_count": 5,
            "recent_releases_count": 1,
            "repo_breakdown": {"repo1": 60}
        }
        
        result = self.agent.analyze(data)
        
        # Verify Health
        self.assertEqual(result["execution_health"], "Declining")
        self.assertEqual(result["severity"], "High")
        
        # Verify Signals
        self.assertEqual(result["signals"]["commit_velocity_change_pct"], -40.0)
        self.assertEqual(result["signals"]["execution_health"], "Declining")
        
    def test_analyze_stable_health(self):
        """Test that 15% drop triggers Stable/Medium severity"""
        # Mock data: Current dropped by 15% compared to Prev
        data = {
            "commit_velocity_current": 85,
            "commit_velocity_prev": 100,
            "active_contributors_count": 10,
            "recent_releases_count": 2,
            "repo_breakdown": {"repo1": 85}
        }
        
        result = self.agent.analyze(data)
        
        self.assertEqual(result["execution_health"], "Stable")
        self.assertEqual(result["severity"], "Medium")
        self.assertEqual(result["signals"]["commit_velocity_change_pct"], -15.0)

    def test_analyze_strong_health(self):
        """Test that flat or positive velocity triggers Strong/Low severity"""
        # Mock data: Current is same as prev
        data = {
            "commit_velocity_current": 100,
            "commit_velocity_prev": 100,
            "active_contributors_count": 15,
            "recent_releases_count": 3,
            "repo_breakdown": {"repo1": 100}
        }
        
        result = self.agent.analyze(data)
        
        self.assertEqual(result["execution_health"], "Strong")
        self.assertEqual(result["severity"], "Low")
        self.assertEqual(result["signals"]["commit_velocity_change_pct"], 0.0)

    def test_confidence_score(self):
        """Test confidence calculation logic"""
        # Confidence = 1 - abs(change_pct)/100
        # -40% change -> 0.6 confidence
        data = {
            "commit_velocity_current": 60,
            "commit_velocity_prev": 100,
            "active_contributors_count": 5,
            "recent_releases_count": 1,
            "repo_breakdown": {"repo1": 60}
        }
        result = self.agent.analyze(data)
        self.assertAlmostEqual(result["confidence"], 0.6)

    def test_release_cadence(self):
        """Test release cadence classification"""
        # 0 releases -> stalled
        data_stalled = {
            "commit_velocity_current": 100, "commit_velocity_prev": 100,
            "active_contributors_count": 5, "recent_releases_count": 0, "repo_breakdown": {}
        }
        self.assertEqual(self.agent.analyze(data_stalled)["signals"]["release_cadence"], "stalled")
        
        # 4 releases -> normal
        data_normal = {
            "commit_velocity_current": 100, "commit_velocity_prev": 100,
            "active_contributors_count": 5, "recent_releases_count": 4, "repo_breakdown": {}
        }
        self.assertEqual(self.agent.analyze(data_normal)["signals"]["release_cadence"], "normal")

if __name__ == '__main__':
    unittest.main()
