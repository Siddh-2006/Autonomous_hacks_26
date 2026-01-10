import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.cto.agent import CTOAgent

class TestCTOLive(unittest.TestCase):
    def setUp(self):
        self.agent = CTOAgent()
        print("\n[CTO] Starting Live GitHub Audit...")

    def test_github_audit(self):
        """Verify GitHub API access and metric calculation."""
        result = self.agent.analyze()
        
        # 1. Check Critical Metrics
        commits = result['signals']['total_commits_last_30d'] # signals dict key from agent.py
        # Wait, let's check agent.py structure. it returns 'signals' inside result?
        # Looking at previous code, `result` HAS `signals` dict.
        # But `metrics` keys were flat in `analyze` variables, let's double check.
        # The agent returns: "signals": {...} which contains 'total_commits_last_30d'?? 
        # Check `backend/agents/cto/agent.py` line 70:
        # "signals": { "commit_velocity_change_pct", "release_cadence", "new_repos_90d", "active_contributors" }
        # Ah, `total_commits` is a top level internal field.
        
        commits = result.get('total_commits') # Top level key
        print(f"[CTO] Commits Last 30d: {commits}")
        
        # We expect a public tech company to have > 0 commits
        self.assertGreater(commits, 0, "CTO Agent found 0 commits. GitHub API might be rate-limited.")
        
        # 2. Check Health Status
        self.assertIn(result['execution_health'], ['Strong', 'Stable', 'Declining'])

if __name__ == '__main__':
    unittest.main()
