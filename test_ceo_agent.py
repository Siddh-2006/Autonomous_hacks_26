import sys
import os
import json

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

# 1. Run CEO Agent
print("\n[TEST] Running CEO Agent...")
from backend.agents.ceo.agent import CEOAgent
agent = CEOAgent()
result = agent.analyze()

print("\n--- CEO AGENT OUTPUT ---")
print(json.dumps(result, indent=2))

# 2. Verify DB Persistence
print("\n[TEST] Verifying Database Storage...")
from backend.db.database import get_latest_ceo_snapshot
snapshot = get_latest_ceo_snapshot()
if snapshot:
    print(f"[PASS] Snapshot saved. ID: {snapshot['id']}, Health: {snapshot['narrative_health']}")
else:
    print("[FAIL] No snapshot found.")
