import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot, get_latest_cpo_snapshot
from backend.reasoning.rules import evaluate_executive_risk

class ExecutiveEvaluator:
    def __init__(self):
        pass
        
    def evaluate_current_state(self):
        # 1. Load Latest Snapshots (The "Board Packet")
        cfo = get_latest_cfo_snapshot() or {}
        ceo = get_latest_ceo_snapshot() or {}
        cto = get_latest_cto_snapshot() or {}
        cpo = get_latest_cpo_snapshot() or {}
        
        # 2. Apply Rules
        verdict = evaluate_executive_risk(cfo, cto, ceo, cpo)
        
        # 3. Add context
        verdict['timestamp'] = cfo.get('timestamp') or ceo.get('timestamp') # Proximate timestamp
        verdict['supporting_data'] = {
            'cfo_mode': cfo.get('financial_mode', 'N/A'),
            'cto_health': cto.get('execution_health', 'N/A'),
            'ceo_health': ceo.get('narrative_health', 'N/A'),
            'cpo_health': cpo.get('product_health', 'N/A')
        }
        
        return verdict
