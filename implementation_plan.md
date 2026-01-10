# Executive Reasoning System Implementation Plan

## Goal
Build a deterministic, rule-based "Executive Reasoning Layer" that aggregates signals from CTO, CFO, and CEO agents to produce an investor-grade risk assessment.

## Architecture
1.  **Internet** (Public Data) -> Agents (CTO/CFO/CEO)
2.  **Agents** (Independent Observers) -> Reasoning Engine
3.  **Reasoning Engine** (Deterministic Rules) -> Executive Snapshot -> Dashboard

## Part 1: CTO Agent (The Missing Link)
*   **Role**: Audit technical innovation and execution health.
*   **Data Source**: GitHub API (`couchbase` organization).
    *   *Metrics*: Commit velocity, active contributors, new repositories.
*   **Logic**:
    *   Commits < Prev Month -> `Declining` (Execution Risk)
    *   New Repos > 0 -> `Strong` (Innovation)
    *   Else -> `Stable`

## Part 2: Reasoning Layer (The Brain)
*   **`backend/reasoning/rules.py`**:
    *   Pure logic functions. e.g. `evaluate_narrative_vs_execution(ceo_signal, cto_signal)`.
    *   Returns `overall_risk` (Low/Medium/High) and `reason` (String).
*   **`backend/reasoning/evaluator.py`**:
    *   Loads latest snapshots from all 3 agents.
    *   Runs through the rule chain.
*   **`backend/agents/executive_reasoning_agent.py`**:
    *   The "System Controller". Triggers agents if needed, runs evaluator, saves result.

## Part 3: Database & Storage
*   **Tables**:
    *   `cto_snapshots` (Metrics, innovation score)
    *   `executive_snapshots` (Risk, confidence, summary)

## Proposed Changes
### Backend / Data Sources
#### [NEW] [github_scraper.py](file:///d:/Autonomous _hacks/auto-diligence/backend/data_sources/github_scraper.py)

### Backend / Agents
#### [NEW] [cto/agent.py](file:///d:/Autonomous _hacks/auto-diligence/backend/agents/cto/agent.py)
#### [NEW] [executive_reasoning_agent.py](file:///d:/Autonomous _hacks/auto-diligence/backend/agents/executive_reasoning_agent.py)

### Backend / Reasoning
#### [NEW] [rules.py](file:///d:/Autonomous _hacks/auto-diligence/backend/reasoning/rules.py)
#### [NEW] [evaluator.py](file:///d:/Autonomous _hacks/auto-diligence/backend/reasoning/evaluator.py)

### Backend / DB
#### [MODIFY] [schema.sql](file:///d:/Autonomous _hacks/auto-diligence/backend/db/schema.sql)
#### [MODIFY] [database.py](file:///d:/Autonomous _hacks/auto-diligence/backend/db/database.py)

## Part 4: Vector Memory & Forensics (Phase 2) [COMPLETED]
*   **Goal**: "Deep Memory" to detect recurring risks and narrative contradictions over years.
*   **Implementation**:
    *   **Engine**: `chromadb` (Local Vector Store).
    *   **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`.
*   **Components**:
    *   **`backend/storage/vector_db.py`**: Wrapper for ChromaDB ingestion and semantic search.
    *   **`backend/storage/seed_archetypes.py`**: Pre-loads "Risk Signatures" (e.g. Bankruptcy announcements) for CFO comparison.
    *   **`backend/vectors/backfill.py`**: Loads historical strategy (2022-2024) for CEO contradiction checks.
    *   **`backend/vectors/evasion_detector.py`**: Prototype for Earnings Call audit.

