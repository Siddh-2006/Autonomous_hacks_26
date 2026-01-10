from datetime import datetime
import sys
import os
import json

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.agents.base_agent import BaseAgent
from backend.reasoning.evaluator import ExecutiveEvaluator
from backend.db.database import get_db_connection

class ExecutiveReasoningAgent(BaseAgent):
    def __init__(self):
        super().__init__("ExecutiveBoard")
        self.evaluator = ExecutiveEvaluator()

    def analyze(self):
        # 1. Run Evaluator (The Brain)
        verdict = self.evaluator.evaluate_current_state()
        
        # 2. Store Result (Tier 3)
        self._store_snapshot(verdict)
        
        return verdict

    def _store_snapshot(self, data):
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO executive_snapshots (
                timestamp, overall_risk, confidence, summary, supporting_agents
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            data['overall_risk'],
            data['confidence'],
            data['reason'],
            json.dumps(data['supporting_data'])
        ))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    agent = ExecutiveReasoningAgent()
    result = agent.analyze()
    print(json.dumps(result, indent=2))
