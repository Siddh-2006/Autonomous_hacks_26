# 🧠 Auto-Diligence: Data & Logic Blueprint

This document reveals the "Internal Wiring" of the system. It details exactly **What Data** is fetched, **Where** it comes from, and the **Exact Logic** used to turn that data into a Board Verdict.

Use this to identify gaps for your Next Version (V2).

---

## 1. The CTO Agent (Engineering Health)
*Does the code match the hype?*

### 📥 Data Source
*   **Source**: GitHub API (via `PyGithub`)
*   **Target**: Public repositories of the company (e.g., `couchbase/couchbase-lite-android`).
*   **Raw Data Fetched**:
    *   List of Repositories (Stars, Forks, Last Update Date).
    *   Commit History (Last 90 days).
    *   Contributor List (Usernames, Commit Counts).
    *   Pull Requests (Open vs Closed).

### ⚙️ The Logic (Risk Engine)
1.  **Zombie Check**:
    *   *Input*: `last_commit_date`
    *   *Rule*: `If last_commit > 60 days ago: Flag "Zombie/Inactive"`.
    *   *Logic*: Healthy software companies code daily.
2.  **Bus Factor (The "Hit by a Bus" Risk)**:
    *   *Input*: `contributors` list.
    *   *Rule*: `If top_1_committer > 80% of lines_changed AND total_contributors < 3`: **HIGH RISK**.
    *   *Logic*: If one person leaves, the product dies.
3.  **Velocity Score**:
    *   *Input*: `commits_90d` / 12 (Weeks).
    *   *Rule*: `If commits_per_week < 2`: **LOW VELOCITY**.

### 🛠️ V2 Opportunity (What to Build)
*   **Code Quality**: Currently, we only count *quantity*. You could add an LLM to read the *content* of the code. (Is it "AI code" or just "Readme updates"?).
*   **Turnover**: Track specific developers. Did the "Top Committer" from 2023 stop coding in 2024? (Churn Signal).

---

## 2. The CFO Agent (Financial Reality)
*Are they spending money like a growing company?*

### 📥 Data Source
*   **Source**: Greenhouse / Lever / Ashby (Career Page Scraping).
*   **Target**: `boards.greenhouse.io/{company}`.
*   **Raw Data Fetched**:
    *   Job Titles ("Senior Engineer", "Sales Intern").
    *   Department Names ("R&D", "G&A").
    *   Total Count of Roles.

### ⚙️ The Logic (Forensic Engine)
1.  **Growth Mode Classification**:
    *   *Input*: `total_open_roles` vs `historical_snapshot` (DB).
    *   *Rule*: `If roles dropped > 10%`: **CONTRACTION** mode. `If roles rose > 10%`: **GROWTH** mode.
2.  **Juniorization Ratio (Cost Cutting Detection)**:
    *   *Input*: Count of "Senior/Staff/Principal" vs "Junior/Intern/Entry".
    *   *Rule*: `If Junior > Senior AND Mode == Contraction`: **QUALITY RISK**.
    *   *Logic*: They are firing expensive pros and hiring cheap grads to save money while pretending to grow.
3.  **Semantic Risk (The "Vibe Check")**:
    *   *Input*: Press Release Text.
    *   *Rule*: `If text contains ["streamlining", "efficiency", "focus"]`: **RISK +1**.

### 🛠️ V2 Opportunity (What to Build)
*   **Salary Estimation**: Scrape job descriptions for "$150k-$200k" ranges. Calculate "Projected Burn Rate".
*   **Ghost Jobs**: Track how long a job stays open. `If > 6 months`: It's a fake job to look like they are growing.

---

## 3. The CEO Agent (Strategic Narrative)
*Is the story consistent or desperate?*

### 📥 Data Source
*   **Source**: Google News RSS Feed.
*   **Target**: Query `"{Company Name} business strategy"`.
*   **Raw Data Fetched**:
    *   Article Titles & Snippets.
    *   Publication Dates.

### ⚙️ The Logic (Contradiction Engine)
1.  **Sentiment Analysis**:
    *   *Input*: News Snippets.
    *   *Logic*: Use `TextBlob` (NLP) to score polarity (-1 to +1).
    *   *Rule*: `If Avg Sentiment < -0.1`: **bad_news_alert**.
2.  **Strategy Shift Detector (Vector Memory)**:
    *   *Input*: Current News ("We are an AI company").
    *   *Memory*: Past 2 years of SEC Filings ("We are a Database company").
    *   *Logic*: Cosine Similarity between vectors.
    *   *Rule*: `If Similarity < 0.6`: **PIVOT DETECTED**. (They changed their story).

### 🛠️ V2 Opportunity (What to Build)
*   **Executive Podcast Analysis**: Transcribe CEO interviews on YouTube. Compare *tone of voice* (Stress detection) vs written PRs.
*   **Insider Trading**: Connect to an SEC API. Did the CEO sell stock right before announcing a "Pivot"?

---

## 4. The Board (The Final Judge)
*The Correlation Matrix*

### ⚙️ The Logic (Rule-Based Systems)
It uses a deterministic set of **Rules** (`backend/reasoning/rules.py`):

*   **FRAUD_RISK**: If CFO says `Contraction` BUT CEO says `Explosive Growth`. (Lying).
*   **HYPE_RISK**: If CEO says `AI Pivot` BUT CTO says `0 AI Libraries` in code. (Vaporware).
*   **DYING**: If CFO `Hiring Freeze` AND CTO `Zombie Code`. (Company is winding down).

---

## Summary of Files & Architecture
*   `backend/data_sources/`: contains the **Scrapers**.
*   `backend/agents/*/agent.py`: contains the **Analysis Logic**.
*   `backend/storage/vector_db.py`: contains the **Strategic Memory**.
*   `backend/reasoning/rules.py`: contains the **Board's Verdict Logic**.
