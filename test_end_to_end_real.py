import sys
import os
import time

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

# 1. Database Setup
from backend.db.database import init_db
print("[TEST] Initializing Database...")
init_db()

# 2. Run CFO Agent (First Run - Baseline)
print("\n[TEST] Running CFO Agent (Cycle 1)...")
from backend.agents.cfo.agent import CFOAgent
agent = CFOAgent()
result1 = agent.analyze()
print(f"Cycle 1 Mode: {result1['financial_mode']}")

# 3. Simulate Time Passing / Change (by manipulating DB or just running again)
# For this test, we accept that running it effectively 'verifies' the scraping and logic pipeline.
# The 'Snapshot' data we added is static, so it will show '0.0%' change if run twice, which is correct for stability.

print("\n[TEST] Running CFO Agent (Cycle 2 - Verification)...")
result2 = agent.analyze()
print(f"Cycle 2 Mode: {result2['financial_mode']}")
print(f"Audit Verdict: {result2['audit_verdict']}")
print(f"Linguistic Score: {result2['signals']['linguistic_risk_score']}")

# 4. Check Output
memo_path = "d:/Autonomous _hacks/auto-diligence/CFO_MEMO.md"
if os.path.exists(memo_path):
    print("\n[PASS] CFO_MEMO.md generated.")
    with open(memo_path, 'r', encoding='utf-8') as f:
        print("--- MEMO PREVIEW ---")
        print(f.read()[:500])
else:
    print("\n[FAIL] CFO_MEMO.md NOT found.")

print("\n[TEST] End-to-End Test Complete.")
