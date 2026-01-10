import traceback
import sys
import os

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

try:
    print("Attempting to import ExecutiveReasoningAgent...")
    from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent
    print("Import successful. Initializing...")
    agent = ExecutiveReasoningAgent()
    print("Analyzing...")
    result = agent.analyze()
    print(result)
except Exception:
    err = traceback.format_exc()
    print(err)
    with open("d:/Autonomous _hacks/auto-diligence/error_log.txt", "w") as f:
        f.write(err)
