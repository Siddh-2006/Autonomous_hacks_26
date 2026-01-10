import sys
import os
import json

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

print("\n--- 1. CEO AGENT (Strategy) ---")
from backend.agents.ceo.agent import CEOAgent
ceo_agent = CEOAgent()
ceo_result = ceo_agent.analyze()
print(f"Health: {ceo_result['narrative_health']} | Severity: {ceo_result['severity']}")

print("\n--- 2. CFO AGENT (Finance) ---")
from backend.agents.cfo.agent import CFOAgent
cfo_agent = CFOAgent()
cfo_result = cfo_agent.analyze()
print(f"Mode: {cfo_result['financial_mode']} | Severity: {cfo_result['severity']}")

print("\n--- 3. CTO AGENT (Tech) ---")
from backend.agents.cto.agent import CTOAgent
cto_agent = CTOAgent()
cto_result = cto_agent.analyze()
print(f"Health: {cto_result['execution_health']} | Severity: {cto_result['severity']}")

print("\n--- 4. EXECUTIVE BOARD (Orchestrator) ---")
from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent
board = ExecutiveReasoningAgent()
verdict = board.analyze()

print("\n=============== FINAL BOARD VERDICT ===============")
print(f"RISK LEVEL: {verdict['overall_risk'].upper()}")
print(f"CONFIDENCE: {verdict['confidence']*100:.1f}%")
print(f"SUMMARY:    {verdict['reason']}")
print("===================================================")

if verdict['overall_risk'] in ['Low', 'Medium', 'High', 'Critical']:
    print("[PASS] System logic is operational.")
else:
    print("[FAIL] Invalid risk output.")
