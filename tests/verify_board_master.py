import sys
import os
import unittest
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.reasoning.rules import evaluate_executive_risk
from backend.reasoning.evaluator import ExecutiveEvaluator

class TestBoardMasterLogic(unittest.TestCase):

    def test_narrative_inflation(self):
        """Test Rule [3.1]: CEO Optimistic + CTO Declining"""
        verdict = evaluate_executive_risk(
            cfo_snapshot={'financial_mode': 'Stable'},
            cto_snapshot={'execution_health': 'Declining'},
            ceo_snapshot={'narrative_health': 'Strong'},
            cpo_snapshot={'product_health': 'Healthy'}
        )
        self.assertEqual(verdict['overall_risk'], 'High')
        self.assertEqual(verdict['risk_type'], 'Narrative')
        print(f"[PASS] Narrative Inflation: {verdict['reason']}")

    def test_death_spiral(self):
        """Test Rule [3.4]: Triple Negative"""
        verdict = evaluate_executive_risk(
            cfo_snapshot={'financial_mode': 'Cost-Control'},
            cto_snapshot={'execution_health': 'Critical'},
            ceo_snapshot={'narrative_health': 'Weakening'},
            cpo_snapshot={'product_health': 'Declining'}
        )
        self.assertEqual(verdict['overall_risk'], 'Critical')
        self.assertEqual(verdict['risk_type'], 'Terminal')
        print(f"[PASS] Death Spiral: {verdict['reason']}")

    def test_evaluator_memory(self):
        """Test Time-Based Memory (requires DB access, mocking for now or running live)"""
        # We'll run the actual evaluator to check schema and execution
        evaluator = ExecutiveEvaluator()
        try:
            result = evaluator.evaluate_current_state()
            print(f"\n[LIVE CHECK] Evaluator Result:")
            print(f"   > Risk: {result['overall_risk']}")
            print(f"   > Type: {result.get('risk_type', 'N/A')}")
            print(f"   > Trend: {result.get('change_from_last_period', 'N/A')}")
            
            self.assertIn('change_from_last_period', result)
            self.assertIn('risk_type', result['supporting_data'])
        except Exception as e:
            self.fail(f"Evaluator Failed: {e}")

if __name__ == '__main__':
    unittest.main()
