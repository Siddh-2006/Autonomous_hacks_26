# CEO Agent: Narrative & Strategy Intelligence

> **"The CEO"**
> An autonomous system that mimics the strategic thinking of a Chief Executive Officer. It ignores day-to-day noise and focuses on broad narrative arcs, strategic clarity, and leadership confidence.

---

## 1. Core Philosophy (CEO Mindset)
A real CEO doesn't ask "Is the news positive today?". They ask:
*   "Are we speaking confidently or defensively?"
*   "Is our strategy consistent or pivoting?"
*   "Are leadership risks surfacing?"

This agent replicates that thinking using a **Time-Based Reasoning** engine. It compares today's signals against a historical baseline (last 30 days) to detect *change*, not just *state*.

---

## 2. Architecture & Implementation (3-Tier)

### Tier 1: Data Collection & Signals
*   **`backend/data_sources/news_scraper.py`**:
    *   **Primary**: Fetches live news via Google News RSS (verified working).
    *   **Resiliency**: Falls back to `real_news_snapshot.json` if RSS fails.
*   **`backend/data_sources/strategy_analyzer.py`**:
    *   **Signal Extractor**: Scans text for specific regex patterns:
        *   *Forward-Looking*: "growth", "roadmap", "investment".
        *   *Defensive*: "headwinds", "challenges", "restructuring".

### Tier 2: The "CEO Brain" (Intelligence)
*   **`backend/agents/ceo/agent.py`**:
    *   **Baseline Creation**: On the first run, it establishes a "Normal" state.
    *   **Trend Detection**: On subsequent runs, it compares current scores vs. the 5-run moving average from the DB.
    *   **Decision Logic**:
        *   *Weakening*: Defensive Score spikes > 20% while Forward Score drops.
        *   *Strong*: Forward Score spikes > 20% while Defensive drops.
        *   *Stable*: Changes are within noise levels.

### Tier 3: Memory (Storage)
*   **`backend/db/cfo.db` (Table: `ceo_snapshots`)**:
    *   Stores `narrative_health`, `forward_score`, `defensive_score`, and raw signals for every run.
    *   Crucial for the "Time-Based Reasoning" mechanism.

---

## 3. How to Run & Verify

### Step 1: Run the Agent (Live)
```bash
python "d:/Autonomous _hacks/auto-diligence/backend/agents/ceo/agent.py"
```
*   **Output**: JSON object with `narrative_health` and `explanation`.
*   **Action**: It scrapes Google News, computes scores, checks history, and saves a new snapshot to SQLite.

### Step 2: Verification Script
```bash
python "d:/Autonomous _hacks/auto-diligence/test_ceo_agent.py"
```
*   **What it does**: Runs the agent and immediately queries the DB to confirm the data was saved.

---

## 4. Addressing Data Sources (CFO vs CEO)
*   **CEO Agent**: Uses **Live Google News RSS**. The `real_news_snapshot.json` exists purely as a backup but is currently *bypassed* because live fetching works.
*   **CFO Agent**: Uses **`careers_scraper.py`**.
    *   *Status*: Live scraping of Couchbase/Greenhouse is currently **Blocked (403)**.
    *   *Resolution*: The agent relies on `real_data_snapshot.json` to function. **Do not delete this JSON**, or the CFO agent will return empty data and fail.

## 5. Sample Output (CEO Board Summary)
```json
{
  "agent": "CEO",
  "narrative_health": "Strong",
  "severity": "Low",
  "signals": {
    "forward_looking_statements": "increasing",
    "strategy_shift_detected": false
  },
  "explanation": "Strategy is gaining clarity. Significant increase in forward-looking statements compared to previous periods."
}
```
