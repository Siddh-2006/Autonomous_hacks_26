import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent

class TestExecutiveBoard(unittest.TestCase):
    def setUp(self):
        self.agent = ExecutiveReasoningAgent()
        print("\n[BOARD] Convening Executive Session...")

    def test_board_logic(self):
        """Verify the Reasoning Engine aggregates signals correctly."""
        result = self.agent.analyze()
        
        print(f"[BOARD] Verdict: {result['overall_risk']}")
        print(f"[BOARD] Confidence: {result['confidence']}")
        print(f"[BOARD] Reason: {result['reason']}")
        
        # 1. Check Output Safety
        self.assertIn(result['overall_risk'], ['Low', 'Medium', 'High', 'Critical'])
        
        # 2. Check Supporting Data
        supporting = result.get('supporting_data', {})
        self.assertIn('cfo_mode', supporting)
        self.assertIn('cto_health', supporting)
        self.assertIn('ceo_health', supporting)

if __name__ == '__main__':
    unittest.main()
