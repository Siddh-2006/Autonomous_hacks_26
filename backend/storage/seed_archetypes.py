import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.storage.vector_db import vector_memory

def seed_risk_archetypes():
    print("[VECTOR] Seeding Forensic Archetypes...")
    
    # 1. Bankruptcy / Distress Signals
    distress_texts = [
        "We have substantial doubt about our ability to continue as a going concern.",
        "We have engaged advisors to explore strategic alternatives including a potential sale.",
        "We are suspending guidance due to market uncertainty.",
        "Liquidity constraints may impact our ability to meet obligations."
    ]
    
    for text in distress_texts:
        vector_memory.store_narrative(
            agent="ARCHETYPE_DISTRESS",
            text=text,
            metadata={"risk_level": "CRITICAL", "type": "DISTRESS"}
        )
        
    # 2. Layoffs / Contraction Signals
    contraction_texts = [
        "We are executing a restructuring plan to reduce operating expenses.",
        "We are streamlining our workforce to align with strategic priorities.",
        "We are pausing hiring to realize operational efficiencies.",
        "Headcount reduction actions were taken in the quarter."
    ]
    
    for text in contraction_texts:
        vector_memory.store_narrative(
            agent="ARCHETYPE_CONTRACTION",
            text=text,
            metadata={"risk_level": "HIGH", "type": "CONTRACTION"}
        )
        
    # 3. Growth / Strength Signals
    growth_texts = [
        "We achieved record revenue growth and expanded margins.",
        "We are accelerating investment in R&D to drive innovation.",
        "Demand remains robust across all geographies.",
        "We are raising guidance for the full fiscal year."
    ]
    
    for text in growth_texts:
        vector_memory.store_narrative(
            agent="ARCHETYPE_GROWTH",
            text=text,
            metadata={"risk_level": "LOW", "type": "GROWTH"}
        )
        
    print("[VECTOR] Seeding Complete. The CFO Agent now has a baseline for comparison.")

if __name__ == "__main__":
    try:
        seed_risk_archetypes()
    except Exception as e:
        print(f"[ERROR] Seeding failed (Dependencies missing?): {e}")
