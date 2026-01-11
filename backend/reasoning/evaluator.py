import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot, get_latest_cpo_snapshot, get_executive_history
from backend.reasoning.rules import evaluate_executive_risk

class ExecutiveEvaluator:
    def __init__(self):
        pass
        
    def evaluate_current_state(self, manual_snapshots=None):
        # 1. Load Snapshots (Real or Simulated)
        if manual_snapshots:
            cfo = manual_snapshots.get('cfo', {})
            ceo = manual_snapshots.get('ceo', {})
            cto = manual_snapshots.get('cto', {})
            cpo = manual_snapshots.get('cpo', {})
        else:
            cfo = get_latest_cfo_snapshot() or {}
            ceo = get_latest_ceo_snapshot() or {}
            cto = get_latest_cto_snapshot() or {}
            cpo = get_latest_cpo_snapshot() or {}
        
        # 2. Apply Rules
        verdict = evaluate_executive_risk(cfo, cto, ceo, cpo)
        
        # 3. Add context (Timestamps & Raw Data)
        verdict['timestamp'] = cfo.get('timestamp') or ceo.get('timestamp') # Proximate timestamp
        verdict['supporting_agents'] = ['CTO', 'CFO', 'CEO', 'CPO']
        
        # 4. TIME-BASED MEMORY (The "Trend Check")
        # Compare vs last verdict to determine "change_from_last_period"
        history = get_executive_history(limit=1)
        prev_risk = "Medium" # Default baseline for first run
        
        if history:
            prev_risk = history[0].get('overall_risk', 'Medium')
            
        # Risk Severity Map for Comparison
        severity_map = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
        current_score = severity_map.get(verdict['overall_risk'], 2)
        prev_score = severity_map.get(prev_risk, 2)
        
        if current_score > prev_score:
            verdict['change_from_last_period'] = 'Worsening'
        elif current_score < prev_score:
            verdict['change_from_last_period'] = 'Improving'
        else:
            verdict['change_from_last_period'] = 'Stable'
            
        # 5. Pack Supporting Data for Audit
        verdict['supporting_data'] = {
            'cfo_mode': cfo.get('financial_mode', 'N/A'),
            'cto_health': cto.get('execution_health', 'N/A'),
            'ceo_health': ceo.get('narrative_health', 'N/A'),
            'cpo_health': cpo.get('product_health', 'N/A'),
            'risk_type': verdict.get('risk_type', 'Mixed')
        }
        
        return verdict
