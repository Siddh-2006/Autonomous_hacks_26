# 🧢 The CPO Agent (Product/Market Reality)

## Core Mission
**"Do users actually care?"**
This agent anchors the "Growth Narrative" (CEO) to "Adoption Reality".

## Mental Model
A real CPO asks:
1.  **Adoption Momentum**: Are users choosing us repeatedly? (Stars/Forks Growth)
2.  **User Pain**: Are they complaining loudly? (Issue Volume)
3.  **Maintainer Responsiveness**: Do we care? (Time-to-Resolution)

## Data Signals (GitHub Scraper)
*   **Adoption**: `total_forks` (Ecosystem size), `new_repos_90d` (Innovation).
*   **Pain**: `issue_pressure` (Open/Closed Ratio).
*   **Responsiveness**: `avg_resolution_time_hours` (Speed of fixes).

## Decision Logic
*   **Healthy**: Adoption UP + Fast Resolution.
*   **Stressed**: High Issues + Fast Resolution (Good problem to have).
*   **Declining**: High Issues + Slow Resolution (>1 Week). OR Low Activity + Weak Ecosystem.

## Integration
*   Feeds into the **Executive Board**.
*   Checks for **"Reality Gaps"**: If CEO says "Explosive Growth" but CPO says "Declining", reliability collapses.

## Cross-Validation Rules (The "Truth Triangle")
The Board compares the CPO against other agents to find "Lies":

1.  **CPO vs CEO (The Reality Gap)**
    *   *CEO*: "We are seeing unprecedented demand!" (Sentiment: Strong)
    *   *CPO*: "Issue volume is flat, Star count is frozen." (Health: Declining)
    *   *Verdict*: **CRITICAL RISK**. Narrative fabrication detected.

2.  **CPO vs CTO (The Zombie Check)**
    *   *CPO*: "Product Health is Healthy" (Lots of issues/stars)
    *   *CTO*: "Zero commits in 3 months" (Health: Declining)
    *   *Verdict*: **HIGH RISK**. Product is being used but not maintained (Technical Debt crisis imminent).

3.  **CPO vs CFO (The Efficiency Check)**
    *   *CPO*: "Massive user complaints (Pain)"
    *   *CFO*: "Cost-Control (Firing support staff)"
    *   *Verdict*: **HIGH RISK**. Cutting costs while the product is on fire.

