import sys
import os
import json

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

# 1. Run CTO Agent
print("\n[TEST] Running CTO Agent (GitHub Audit)...")
from backend.agents.cto.agent import CTOAgent
agent = CTOAgent()
result = agent.analyze()

print("\n--- CTO AGENT OUTPUT ---")
print(json.dumps(result, indent=2))

# 2. Verify DB Persistence
print("\n[TEST] Verifying Database Storage...")
from backend.db.database import get_latest_cto_snapshot
snapshot = get_latest_cto_snapshot()
if snapshot:
    print(f"[PASS] Snapshot saved. ID: {snapshot['id']}, Health: {snapshot['execution_health']}")
    print(f"       Details: {snapshot['explanation']}")
else:
    print("[FAIL] No snapshot found.")
