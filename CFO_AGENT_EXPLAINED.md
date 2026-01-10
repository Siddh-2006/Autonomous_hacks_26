# CFO Agent: Architecture & Implementation Explained

This document details exactly what has been built for the Autonomous CFO Agent, following the 3-tier design pattern.

## 🎯 Core Objective
The CFO Agent is designed to **infer the financial health** of a company (specifically monitoring "Growth" vs "Cost-Control" modes) by observing **public hiring signals** rather than internal financial data.

## 🏗️ The 3-Tier Architecture

We built this system in three distinct layers to ensure clarity, scalability, and stability.

### Tier 1: Data Collection Layer
**Responsibility:** Fetch raw facts from the real world. No thinking, just gathering.

- **`backend/data_sources/careers_scraper.py`**:
  - **What it does**: Simulates visiting the Couchbase careers page to get a list of current open job titles.
  - **Status**: Currently uses a *mock* list of roles to ensure stable testing without relying on live website structure updates.
  - **Output**: A list of strings (e.g., `['Senior Engineer', 'Sales Rep']`).

- **`backend/data_sources/role_classifier.py`**:
  - **What it does**: Takes the raw list of titles and buckets them into functional categories: **Engineering**, **Sales**, **Operations**, and **Other**.
  - **Why**: To see *where* the money is going. Engineering hiring = R&D investment; Sales hiring = Growth push; Ops hiring = Scaling overhead.

### Tier 2: Intelligence Layer
**Responsibility:** "Think" like a CFO. Analyze trends, apply logic, and produce a judgment.

- **`backend/agents/cfo/agent.py`**:
  - **The Brain**: This is the core `CFOAgent` class.
  - **Logic Flow**:
    1.  **Read History**: usage `get_latest_snapshot()` from Tier 3 to see what the hiring numbers were *last time*.
    2.  **Compare**: Calculates the percentage change in open roles.
    3.  **Decide**:
        - **Drop > 30%**: Triggers **"Cost-Control"** mode (High Severity).
        - **Drop 10-30%**: Triggers **"Stable"** mode (Medium Severity).
        - **Else**: Triggers **"Growth"** mode.
  - **Output**: Generates a structured JSON signal containing the decision, confidence score, and clear explanation.

### Tier 3: Storage Layer
**Responsibility:** Be the single source of truth. Remember history so changes can be detected.

- **`backend/db/schema.sql`**:
  - Defines the `cfo_snapshots` table structure.
  - Columns include: `open_roles`, `role_change_pct`, `financial_mode`, `alert_severity`, etc.

- **`backend/db/database.py`**:
  - A lightweight wrapper around **SQLite**.
  - Handles connecting to the file-based database (`cfo.db`), initiating the table if it's missing, and saving new agent snapshots.

## 🔄 End-to-End Flow

1.  **Execution**: You run `agent.py`.
2.  **Tier 1**: It asks the Scraper for current roles and the Classifier to sort them.
3.  **Tier 3**: It asks the Database for the *last* known state.
4.  **Tier 2**: The Agent calculates the difference (e.g., "We had 100 roles, now we have 90. That's a 10% drop.").
5.  **Tier 2**: The Agent determines the mode (e.g., "Stable") and assigns a confidence score.
6.  **Tier 3**: The resulting snapshot is saved back to the Database, ready for the dashboard or next run.

## 📁 Key Files Summary

| File Path | Layer | Purpose |
| :--- | :--- | :--- |
| `backend/data_sources/careers_scraper.py` | Tier 1 | Get raw job data. |
| `backend/data_sources/role_classifier.py` | Tier 1 | Organize data into categories. |
| `backend/agents/cfo/agent.py` | Tier 2 | The "Brain" - logic and decision making. |
| `backend/db/database.py` | Tier 3 | Interface to SQLite. |
| `backend/db/schema.sql` | Tier 3 | Database structure definition. |
