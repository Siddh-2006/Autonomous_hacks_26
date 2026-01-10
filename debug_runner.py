import traceback
import sys
import os

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

try:
    print("Attempting to import CFOAgent...")
    from backend.agents.cfo.agent import CFOAgent
    print("Import successful. Initializing...")
    agent = CFOAgent()
    print("Analyzing...")
    result = agent.analyze()
    print(result)
except Exception:
    err = traceback.format_exc()
    print(err)
    with open("d:/Autonomous _hacks/auto-diligence/error_log.txt", "w") as f:
        f.write(err)
