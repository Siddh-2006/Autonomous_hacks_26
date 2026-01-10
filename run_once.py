import sys
import os
from datetime import datetime

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.cto.agent import CTOAgent
from backend.agents.cfo.agent import CFOAgent
from backend.agents.ceo.agent import CEOAgent
from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent

def run_pipeline():
    print(f"\n[SCHEDULER] Starting Executive Audit at {datetime.now().isoformat()}...")
    
    try:
        # 1. Run Core Agents
        print("  > Running CFO Agent...")
        cfo = CFOAgent().analyze()
        print(f"    [CFO] Mode: {cfo.get('financial_mode', 'N/A')}")
        
        print("  > Running CEO Agent...")
        ceo = CEOAgent().analyze()
        print(f"    [CEO] Health: {ceo.get('narrative_health', 'N/A')}")
        
        print("  > Running CTO Agent...")
        cto = CTOAgent().analyze()
        print(f"    [CTO] Health: {cto.get('execution_health', 'N/A')}")
        
        # 2. Run Executive Board (The Reasoning Layer)
        print("  > Convening Executive Board...")
        board = ExecutiveReasoningAgent().analyze()
        print(f"    [BOARD] Verdict: {board.get('overall_risk', 'UNKNOWN')}")
        
        print(f"[SCHEDULER] Audit Complete.\n")
        
    except Exception as e:
        print(f"[SCHEDULER] Error in pipeline: {e}")

if __name__ == "__main__":
    run_pipeline()
