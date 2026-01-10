# CFO Agent: Master Guide & Forensic Manual

> **"The Real CFO"**
> An autonomous system that mimics the decision-making and forensic audit capabilities of a Chief Financial Officer using public data.

---

## 1. System Philosophy

This agent is not just a calculator; it is a **Forensic Auditor**. It operates on the principle of **"Trust, but Verify"**.
*   **Trust**: What management says in Press Releases (detected by `linguistic_analyzer.py`).
*   **Verify**: What the company actually does in hiring (detected by `careers_scraper.py` and `role_classifier.py`).

**The Core Formula:**
> IF `Narrative` = "Growth" AND `Behavior` = "Cost-Cutting" THEN `Signal` = **DECEPTION / RISK**

---

## 2. Architecture Overview (3-Tier)

### Tier 1: The "Eyes" (Data Collection)
*   **`backend/data_sources/careers_scraper.py`**:
    *   Attempts to scrape live data from Couchbase Careers.
    *   *Resilience*: Automatically falls back to `real_data_snapshot.json` if pushed back by anti-bot protections.
*   **`backend/data_sources/role_classifier.py`**:
    *   **Function Classification**: Engineering, Sales, Ops.
    *   **Seniority Analysis**: Detects "Juniorization" (Exec vs. Associate ratios).
*   **`backend/data_sources/linguistic_analyzer.py`**:
    *   Scans text for "Hedging" (e.g., "we aim to") and "Passive Voice".

### Tier 2: The "Brain" (Intelligence)
*   **`backend/agents/cfo/agent.py`**:
    *   Aggregates Tier 1 data.
    *   Compares vs. Tier 3 History.
    *   **Forensic Logic**:
        *   Checks for **Narrative Disconnects** (High Linguistic Risk + Hiring Freeze).
        *   Checks for **Quality of Earnings** (Replacing VPs with Interns).
    *   Generates the **Board Memo**.

### Tier 3: The "Memory" (Storage)
*   **`backend/db/cfo.db`**: SQLite database storing every run's snapshot.
*   **`backend/db/schema.sql`**: Immutable record of truth.

---

## 3. How to Run & Test

### Run the Agent (Standard Operation)
```bash
python "d:/Autonomous _hacks/auto-diligence/backend/agents/cfo/agent.py"
```
*   **Output**: JSON Signal to console + saves to DB + generates `CFO_MEMO.md`.

### Run the End-to-End Test Suite
```bash
python "d:/Autonomous _hacks/auto-diligence/test_end_to_end_real.py"
```
*   **What it does**:
    1.  Initializes Database.
    2.  Runs Agent Cycle 1 (Baseline).
    3.  Runs Agent Cycle 2 (Verification).
    4.  Verifies `CFO_MEMO.md` creation.

---

## 4. The Output: Board Memo

The agent communicates via a structured markdown memo found at `auto-diligence/CFO_MEMO.md`.

**Example Output:**
> **SUBJECT:** Financial Health & Narrative Integrity Audit
> **Forensic Signals:**
> *   **Linguistic Integrity:** Score 5 (Caution).
> *   **Auditor Recommendation:** Monitor for divergence between PRs and Hiring.

---

## 5. Future Roadmap
*   **LinkedIn Integration**: For truer "Departures" data.
*   **Glassdoor Sentiment**: To catch internal morale drops before they hit the news.
*   **Multi-Company Support**: Scaling the DB schema for ticker-based tracking.
