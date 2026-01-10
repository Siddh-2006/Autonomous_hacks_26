# CFO Database Expansion Strategy 📈

To make the CFO Agent "Hedge Fund Grade", we must move beyond simple hiring metrics. Here is the roadmap to expand the Database for maximum **Intelligence Efficiency**.

## 1. Earnings Call Transcripts (The "Truth Serum") 🗣️
Press Releases are written by Marketing. Earnings Call Q&A sessions are where the truth slips out.
*   **Data Source**: SeekingAlpha / Quartr / EarningsCast (or mock for now).
*   **Vector DB Usage**: **"Evasion Detection"**.
    *   *Logic*: Measure the Semantic Similarity between the **Analyst's Question** and the **CFO's Answer**.
    *   *Signal*: If Similarity < 0.3, the CFO **evaded** the question.
    *   *Example*:
        *   Q: "Are margins compressing?"
        *   A: "We are excited about our AI roadmap."
        *   **Similarity: LOW (Red Flag)**.

## 2. Insider Trading (Form 4) 📂
*   **Data Source**: SEC EDGAR (Form 4).
*   **SQL DB Usage**: New table `insider_trades`.
*   **Logic**:
    *   If `CFO_Sentiment == "Growth"` AND `Net_Insider_Selling > $5M`:
    *   **Signal**: "Pump and Dump" Risk.

## 3. The "Shadow Ledger" (Guidance vs. Reality) 📉
*   **Data Source**: Historical 10-Q Guidance.
*   **Vector/SQL Hybrid**:
    *   Store "Guidance Promises" in Vector DB.
    *   Compare with next quarter's "Actuals".
    *   **Signal**: "Credibility Score" (How often do they miss?).

## Recommendation: Start with Transcripts 🎤
Adding Earnings Transcripts gives the highest "Intelligence per Byte". It captures the raw, unscripted risks.
I can implement a **"Q&A Evasion Detector"** relative to the Vector DB right now.
