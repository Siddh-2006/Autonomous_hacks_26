import sys
import os

# Add project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.storage.vector_db import vector_memory

def check_evasion():
    print("\n--- CFO FORENSICS: Earnings Call Evasion Detector ---")
    
    # 1. The Scenario
    question = "Can you comment on the compression in gross margins this quarter?"
    
    # A generic, evasive answer typical of struggling companies
    evasive_answer = "We are really excited about the long-term opportunity in our AI platform and the customer momentum we are seeing."
    
    # A direct answer
    direct_answer = "Yes, margins compressed by 200bps due to higher cloud infrastructure costs."
    
    print(f"[SCENARIO] Analyst asks: '{question}'")
    
    # 2. Vector Analysis
    # We treat the Question as the 'Query' and the Answer as the 'Document'
    # High semantic similarity implies they are talking about the same topic.
    
    # Note: We need to use the embedding function directly for raw comparison, 
    # but using the collection query is a proxy. 
    # Better: Embed both, calculate distance.
    
    print("\n[ANALYSIS 1] Testing Evasive Answer...")
    # We cheat slightly by storing the answer effectively as a doc and querying it
    # Ideally we'd use cosine_similarity(embed(q), embed(a))
    
    # Let's use the DB to store the answer as a reference, then query with the question
    vector_memory.store_narrative("EARNINGS_CALL_Q3", evasive_answer, {"type": "ANSWER", "status": "EVASIVE"})
    
    results = vector_memory.collection.query(
        query_texts=[question],
        n_results=1,
        where={"agent": "EARNINGS_CALL_Q3"}
    )
    
    dist_evasive = results['distances'][0][0]
    print(f"   > Answer: '{evasive_answer}'")
    print(f"   > Semantic Distance: {dist_evasive:.4f}")
    
    if dist_evasive > 1.3: # Heuristic
        print("   > VERDICT: 🚩 EVASION DETECTED (Subject change)")
    else:
        print("   > VERDICT: Direct Answer")
        
    print("\n[ANALYSIS 2] Testing Direct Answer...")
    vector_memory.store_narrative("EARNINGS_CALL_Q3", direct_answer, {"type": "ANSWER", "status": "DIRECT"})
    
    results = vector_memory.collection.query(
        query_texts=[question],
        n_results=1,
        where={"agent": "EARNINGS_CALL_Q3"}
    ) # Note: this query is fuzzy might pick the old one if we don't filter distinct, 
      # but Chroma usually picks distinct if IDs differ. 
      # Actually, query returns top N. We should rely on the text match.
    
    # Re-querying to find the DIRECT one specifically (simulation limitation)
    # Real logic: Embed(Q) vs Embed(A).
    # Since we lack raw embed access easily via the wrapper, we rely on the query distance
    
    # Let's find the 'Direct' doc we just stored
    # Implementation detail: 'where' clause filtering by metadata helpful if we had unique IDs
    # For this demo, we assume the query finds the closest match.
    
    dist = results['distances'][0][0]
    match_text = results['documents'][0][0]
    
    print(f"   > Closest Match: '{match_text}'")
    print(f"   > Semantic Distance: {dist:.4f}")
    
    if dist < 1.0:
        print("   > VERDICT: ✅ DIRECT ANSWER")

if __name__ == "__main__":
    check_evasion()
