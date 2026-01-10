import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.storage.vector_db import vector_memory

def test_vectors():
    print("\n[TEST] Initializing Vector DB...")
    
    # 1. Test Storage
    print("[TEST] Storing Mock Narratives...")
    vector_memory.store_narrative(
        "CEO", 
        "We are aggressively expanding into AI markets.", 
        {"sentiment": "positive"}
    )
    vector_memory.store_narrative(
        "CFO", 
        "We are cutting costs to preserve cash runway.", 
        {"sentiment": "negative"}
    )
    
    # 2. Test Semantic Search
    print("[TEST] Querying: 'Are we growing?'")
    results = vector_memory.find_similar_events("Are we growing?", n=1)
    
    doc = results['documents'][0][0]
    meta = results['metadatas'][0][0]
    
    print(f"\n[MATCH] Text: {doc}")
    print(f"[MATCH] Agent: {meta['agent']}")
    
    if "expanding" in doc:
        print("[PASS] Semantic Search worked! (Found expansion narrative)")
    else:
        print("[FAIL] Semantic match poor.")

if __name__ == "__main__":
    test_vectors()
