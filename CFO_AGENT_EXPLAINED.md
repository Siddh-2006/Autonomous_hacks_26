# CFO Agent: The Financial Forensic Investigator 🕵️‍♂️💸

## 1. Philosophy
The CFO Agent is not an accountant; it is a **Forensic Auditor**.
It does not just look at "Revenue"; that is backward-looking.
It looks for **"Disconnects"**:
*   *Why did you say "Growth" but freeze hiring?*
*   *Why did you ignore the analyst's question about margins?*
*   *Why does your language sound like a bankruptcy filing?*

## 2. Architecture & Data Sources

### A. Employment Data (The "Real" Ledger)
*   **Source**: Greenhouse API (Live).
*   **Signal**: `open_roles`. A sudden drop in Open Roles (-20%) often predicts a "Missed Quarter" **6 months before the stock drops**.
*   **Data Point**: Cost-Control vs. Growth Mode.

### B. Earnings Call Forensics (The Truth Serum) [NEW]
*   **Source**: Earnings Transcripts (SeekingAlpha/Quartr Simulation).
*   **Logic**: **Vector-Based Evasion Detection**.
    *   We simulate an Analyst asking a hard question (e.g., "Why are margins dropping?").
    *   We measure the **Semantic Distance** of the CFO's answer.
    *   **Threshold**: If Distance > 1.25, the CFO changed the subject.
    *   **Alert**: `[EARNINGS ALERT: Evasive Answer Detected]`.

### C. Risk Archetypes (Vector Memory)
*   **Source**: Historical Bankruptcy Announcements.
*   **Logic**:
    *   The Vector DB holds "Signatures" of distressed companies.
    *   Every Press Release is compared against these signatures.
    *   Matches trigger a **"Semantic Risk Alert"**.

## 3. Decision Logic (Reasoning Layer)
The CFO Agent outputs a `financial_mode` and `audit_verdict`.

| Mode | Condition | Verdict |
| :--- | :--- | :--- |
| **Growth** | Hiring Up + Positive Tone | `Clear` |
| **Stable** | Hiring Flat + Neutral Tone | `Clear` |
| **Cost-Control** | Hiring Down (-10%) | `Caution` |
| **Distress** | Hiring Frozen + Evasive Answers | `CRITICAL` |

## 4. Usage
The CFO Agent runs automatically via the Scheduler.
To verify logic directly:
```bash
python verify_cfo.py
```
