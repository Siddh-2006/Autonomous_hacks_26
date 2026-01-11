# Board / Cross-Agent Executive Reasoning Layer
*Authoritative Master Specification*

## System Role
The **Board Agent** is the "Judge". It does not collect data; it reasons over the verdicts of the C-Suite Agents (CEO, CTO, CFO, CPO).

## 1. Core Question
**"Given everything we know, what is the real risk posture of this company right now?"**

## 2. Input Contract
The Board consumes:
1.  **CTO** (Execution Health, Velocity)
2.  **CFO** (Financial Mode, Burn)
3.  **CEO** (Strategic Narrative, Sentiment)
4.  **CPO** (Product Reality, User Pain)

## 3. Core Risk Dimensions (The Rules)

### 3.1 Narrative Inflation Risk
*   **Pattern**: CEO = `Strong` BUT (CTO = `Declining` OR CPO = `Declining`)
*   **Meaning**: Company is overselling reality.
*   **Verdict**: `High Risk` (Narrative)

### 3.2 Execution Decay Risk
*   **Pattern**: CTO = `Declining` AND CFO = `Cost-Control`
*   **Meaning**: Operational stress with no resources to fix it.
*   **Verdict**: `High Risk` (Execution)

### 3.3 Product-Market Disconnect
*   **Pattern**: CPO = `Declining` BUT CEO = `Strong`
*   **Meaning**: Users are leaving, but CEO is cheering. PMF is lost.
*   **Verdict**: `Critical Risk` (Product)

### 3.4 Terminal Risk (The Death Spiral)
*   **Pattern**: CTO = `Zombie` AND CFO = `Cost-Control` AND CPO = `Declining`
*   **Meaning**: Minimizing burn while the product dies.
*   **Verdict**: `Critical Risk` (Terminal)

### 3.5 The Golden Path (Ideal)
*   **Pattern**: All Agents = `Healthy` / `Strong` / `Growth`
*   **Verdict**: `Low Risk` (Growth)

## 4. Time-Based Memory
The Board **MUST** compare the current verdict to the previous one (Last 6 hours).
*   *Improving*: Risk Level went Down (e.g., High -> Medium).
*   *Worsening*: Risk Level went Up (e.g., Low -> Medium).
*   *Stable*: No change.

## 5. Output Schema
```json
{
  "agent": "BOARD",
  "overall_risk": "Low | Medium | High | Critical",
  "risk_type": "Execution | Narrative | Financial | Product | Mixed",
  "confidence": 0.0,
  "summary": "Plain English verdict.",
  "supporting_agents": ["CTO", "CFO", "CEO", "CPO"],
  "change_from_last_period": "Improving | Stable | Worsening",
  "timestamp": "ISO-8601"
}
```

## 6. Principles
*   **One negative outweighs positives.**
*   **Contradictions are fatal.**
*   **Silence (Zombie CTO) is worse than noise.**
