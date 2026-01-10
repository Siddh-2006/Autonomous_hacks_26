import sys
import os

# Add project root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.agents.ceo.agent import CEOAgent
from backend.storage.vector_db import vector_memory

def test_contradiction():
    print("\n--- TEST: CEO Contradiction Detection ---")
    
    # 1. Setup Mock Baseline in Vector DB (simulating the backfill)
    print("[TEST] Setting up 2023 Baseline: 'We are focusing on profitability.'")
    vector_memory.store_narrative(
        agent="CEO_ARCHIVE",
        text="We are prioritizing efficiency and profitability over growth.",
        metadata={"timestamp": "2023-01-01", "type": "STRATEGIC_BASELINE"}
    )
    
    # 2. Run CEO Logic with a CONTRADICTORY statement
    # The agent normally fetches live news. We will override the analyze method or 
    # just manually check the query logic if possible. 
    # To test the agent *code* itself, we can instantiate it.
    
    agent = CEOAgent()
    
    # Mock the internal logic by manually calling the vector check 
    # (since we can't easily force Google News to give us a specific contradiction)
    
    current_statement = "We are spending aggressively to acquire market share."
    print(f"[TEST] Current Statement: '{current_statement}'")
    
    # The logic inside agent.py is:
    print("[TEST] Running Vector Query (simulating agent internals)...")
    baseline_match = vector_memory.collection.query(
        query_texts=[current_statement],
        n_results=1,
        where={"agent": "CEO_ARCHIVE"}
    )
    
    if baseline_match and baseline_match['documents']:
        dist = baseline_match['distances'][0][0]
        text = baseline_match['documents'][0][0]
        print(f"[RESULT] Closest Match: '{text}'")
        print(f"[RESULT] Distance: {dist}")
        
        # Calibration: Chroma L2 distance for these might be 0.4-0.8
        # We need to know what constitutes a "Contradiction".
        if dist > 0.4: # Lower threshold to catch subtle drift
             print("[PASS] Contradiction Detected! (Distance > 0.4)")
        else:
             print("[FAIL] Contradiction NOT detected. Distance is too low.")
    else:
        print("[FAIL] No baseline found.")

if __name__ == "__main__":
    test_contradiction()
