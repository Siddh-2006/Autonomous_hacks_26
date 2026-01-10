from datetime import datetime
import sys
import os

# Add parent directory to path to allow imports if running as script
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from backend.agents.base_agent import BaseAgent
from backend.data_sources.careers_scraper import fetch_open_roles, fetch_latest_press_release
from backend.data_sources.role_classifier import classify_roles, analyze_seniority
from backend.data_sources.linguistic_analyzer import LinguisticAnalyzer
from backend.db.database import get_latest_cfo_snapshot as get_latest_snapshot, insert_cfo_snapshot as insert_snapshot
from backend.storage.vector_db import vector_memory
from backend.data_sources.earnings_mock import fetch_latest_earnings_call

class CFOAgent(BaseAgent):
    def __init__(self):
        super().__init__("CFO")
        self.linguist = LinguisticAnalyzer()

    def analyze(self):
        # 1. Collect Data (Tier 1)
        current_roles = fetch_open_roles()
        role_counts = classify_roles(current_roles)
        seniority_counts = analyze_seniority(current_roles)
        total_open_roles = len(current_roles)
        
        # Real Data: Fetching Press Release Text
        latest_pr_text = fetch_latest_press_release()
        linguistic_analysis = self.linguist.analyze_text(latest_pr_text)

        # Calculate percentages
        eng_pct = (role_counts['engineering'] / total_open_roles) * 100 if total_open_roles > 0 else 0
        sales_pct = (role_counts['sales'] / total_open_roles) * 100 if total_open_roles > 0 else 0
        ops_pct = (role_counts['ops'] / total_open_roles) * 100 if total_open_roles > 0 else 0
        
        # Seniority Ratios
        junior_heavy = (seniority_counts['junior'] + seniority_counts['entry']) > (seniority_counts['senior'] + seniority_counts['exec'])

        # 2. Retrieve History (Tier 3)
        last_snapshot = get_latest_snapshot()
        
        # 3. Apply Intelligence (Tier 2) - "The Forensic Audit"
        role_change_pct = 0.0
        financial_mode = "Growth"
        severity = "Low"
        audit_verdict = "Clear"
        explanation = "Initial baseline established."
        
        if last_snapshot and last_snapshot['open_roles'] > 0:
            prev_roles = last_snapshot['open_roles']
            role_change_pct = ((total_open_roles - prev_roles) / prev_roles) * 100
            
            # Base Financial Mode
            if role_change_pct < -30:
                financial_mode = "Cost-Control"
            elif role_change_pct < -10:
                financial_mode = "Stable"
            else:
                financial_mode = "Growth"

            # 🚨 FORENSIC LOGIC: Narrative Disconnect Check
            narrative_risk = linguistic_analysis['linguistic_risk_score'] > 2
            
            if narrative_risk and financial_mode == "Cost-Control":
                audit_verdict = "Narrative Disconnect"
                severity = "High"
                explanation = "CRITICAL: Management language shows stress (hedging/passive) and hiring has contracted, contradicting safe growth narratives."
            elif junior_heavy and financial_mode == "Cost-Control":
                audit_verdict = "Juniorization"
                severity = "Medium"
                explanation = "Replacing senior talent with junior roles while cutting costs. Quality of Earnings risk."
            elif financial_mode == "Cost-Control":
                severity = "High"
                explanation = f"Significant drop in open roles ({role_change_pct:.1f}%). Material contraction."
            else:
                explanation = "Operations appear consistent with statements."

        # 🚨 FORENSIC LOGIC II: Earnings Call Evasion Check
        # Generate a baseline "Evasion Score"
        earnings_data = fetch_latest_earnings_call()
        evasion_count = 0
        evasion_details = []
        
        for qa in earnings_data['qa_pairs']:
            # We treat Question similarity to Answer. 
            # If Q and A are discussing different topics (low similarity), it's evasion.
            # Ideally we embed both. Here we Query(Answer) using Q as query text.
            
            try:
                # 1. Store Answer temporarily (or permanently as record)
                vector_memory.store_narrative("TEMP_EARNINGS", qa['answer'], {"type": "ANSWER"})
                
                # 2. Check distance
                match = vector_memory.collection.query(query_texts=[qa['question']], n_results=1, where={"agent": "TEMP_EARNINGS"})
                dist = match['distances'][0][0]
                
                if dist > 1.25: # Tuned Threshold
                    evasion_count += 1
                    evasion_details.append(f"Evaded '{qa['question'][:30]}...' (Dist: {dist:.2f})")
            except:
                pass
        
        if evasion_count > 0:
            severity = "High"
            explanation += f" [EARNINGS ALERT: {evasion_count} Evasive Answers Detected]"
            audit_verdict = "Evasive Management"

        # 4. Construct Signal & Memo
        signal = {
            "agent": "CFO",
            "financial_mode": financial_mode,
            "severity": severity,
            "confidence": 0.95,
            "signals": {
                "open_roles": total_open_roles,
                "role_change_pct": role_change_pct,
                "linguistic_risk_score": linguistic_analysis['linguistic_risk_score'],
                "seniority_mix": seniority_counts
            },
            "audit_verdict": audit_verdict,
            "explanation": explanation,
            "timestamp": datetime.now().isoformat()
        }
        
        # Generate the Board Memo
        self.generate_memo(signal)
        
        # 5. Store Result (Tier 3)
        snapshot_data = {
            "open_roles": total_open_roles,
            "role_change_pct": role_change_pct,
            "engineering_roles_pct": eng_pct,
            "sales_roles_pct": sales_pct,
            "ops_roles_pct": ops_pct,
            "financial_mode": financial_mode,
            "severity": severity,
            "confidence": signal["confidence"],
            "explanation": f"[{audit_verdict}] {explanation}"
        }
        # 6. Vector Memory & Semantic Risk Check
        try:
            # A. Check against Risk Archetypes (The 'Benefit' of Vector DB)
            matches = vector_memory.find_similar_events(explanation, n=1)
            if matches and matches['documents']:
                top_match_text = matches['documents'][0][0]
                top_match_meta = matches['metadatas'][0][0]
                
                # If we match a high-risk archetype with high similarity (heuristic check)
                if top_match_meta.get('agent') in ['ARCHETYPE_DISTRESS', 'ARCHETYPE_CONTRACTION']:
                    print(f"[CFO SEMANTIC ALERT] Logic matches known risk pattern: '{top_match_meta.get('type')}'")
                    # We could escalate severity here, but for now we just log/augment
                    explanation += f" [SEMANTIC MATCH: {top_match_meta.get('type')}]"

            # B. Store the new memory
            vector_memory.store_narrative(
                agent="CFO",
                text=f"{explanation} (PR Text Snippet: {latest_pr_text[:200]}...)",
                metadata={
                    "mode": financial_mode,
                    "severity": severity,
                    "audit_verdict": audit_verdict
                }
            )
        except Exception as e:
            print(f"[WARNING] Vector ops failed: {e}")

        return signal

    def generate_memo(self, signal):
        memo = f"""
# 📉 CFO FORENSIC AUDIT MEMO
**DATE:** {signal['timestamp']}
**TO:** Board of Directors
**FROM:** Autonomous CFO Agent
**SUBJECT:** Financial Health & Narrative Integrity Audit

## 1. Executive Summary
**Current Mode:** {signal['financial_mode']}
**Risk Severity:** {signal['severity']} ({signal['audit_verdict']})

{signal['explanation']}

## 2. Forensic Signals
*   **Hiring Velocity:** {'Dropping' if signal['signals']['role_change_pct'] < 0 else 'Stable/Growing'} ({signal['signals']['role_change_pct']:.1f}% change)
*   **Linguistic Integrity:** Score {signal['signals']['linguistic_risk_score']} (Scale 0-10). Higher score indicates more hedging/passive voice.
*   **Talent Mix:** {signal['signals']['seniority_mix']}

## 3. Auditor Recommendation
Monitor for further divergence between management statements (Press Releases) and operational reality (Hiring/Spending).
"""
        with open("d:/Autonomous _hacks/auto-diligence/CFO_MEMO.md", "w", encoding="utf-8") as f:
            f.write(memo)

if __name__ == "__main__":
    agent = CFOAgent()
    result = agent.analyze()
    print(result)
