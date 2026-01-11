# Scenario Simulation & Decision Control Layer (Master Specification)

**System Role**: Principal AI Architect + Investment Committee Strategist  
**Core Purpose**: Stress-test executive intelligence by asking "What if?".  

---

## 1. Core Question
*"If conditions change, how would the executive verdict change?"*

This is **not prediction**. It is **controlled reasoning under assumptions**.  
This layer elevates the system from a "Dashboard" (Monitoring) to a "Decision Surface" (War-Gaming).

---

## 2. Design Philosophy
### ✅ This Layer IS:
*   **Deterministic**: Same input + same scenario = exact same output.
*   **Transparent**: The user knows exactly what assumptions changed.
*   **Explainable**: The Board must explain *why* the new data changed its mind.
*   **Reversible**: Production state is **never** touched.

### ❌ This Layer is NOT:
*   A forecasting engine (ML/Time-series).
*   A prediction of the future.
*   A data scraper (No external calls in Sim Mode).

---

## 3. High-Level System Flow
```mermaid
graph TD
    UserInput[User Selects Scenario] --> Controller[Scenario Controller]
    Controller -->|Injects Overrides| Agents
    
    subgraph "The Executive Board (Simulated)"
        Agents[CTO / CFO / CEO / CPO Agents] -->|Reasoning with Overrides| Board[Board Reasoning Agent]
    end
    
    Board -->|Simulated Verdict| Dashboard[Dashboard (Simulation View)]
```
*Constraint*: No real database writes. No external API calls. Pure logic execution.

---

## 4. Scenario Types (V1 Scope)
The system supports specific, named stress tests defined in `definitions.json`:

### 4.1 Execution Stress ("The Stalled Engine")
*   **Assumption**: Engineering slows down significantly.
*   **Overrides**:
    *   CTO: Commit Velocity ↓ 35%
    *   CTO: Bus Factor Risk = High

### 4.2 Financial Stress ("The Cash Crunch")
*   **Assumption**: Hiring freezes to preserve runway.
*   **Overrides**:
    *   CFO: New Roles = 0
    *   CFO: Financial Mode = "Cost-Control"

### 4.3 Product Stress ("The Revolt")
*   **Assumption**: Users are unhappy with recent changes.
*   **Overrides**:
    *   CPO: Issue Volume ↑ 50%
    *   CPO: Sentiment = "Negative"

### 4.4 Narrative Stress ("The Pivot")
*   **Assumption**: Leadership becomes defensive.
*   **Overrides**:
    *   CEO: Narrative Tone = "Defensive"

### 4.5 Composite Crisis ("The Death Spiral")
*   **Assumption**: Everything goes wrong at once.
*   **Overrides**: All of the above combined.

---

## 5. Scenario Input Model (Strict)
Scenarios are defined as strict JSON objects. No randomness.

```json
{
  "scenario_name": "Execution Slowdown",
  "overrides": {
    "CTO": {
      "commit_velocity_status": "Declining",
      "bus_factor_risk": true
    },
    "CFO": null,
    "CEO": null,
    "CPO": null
  }
}
```

---

## 6. Scenario Controller Architecture
A new component `ScenarioController` (`backend/scenarios/controller.py`):
1.  **Receives Request**: `POST /api/board/simulate { "scenario": "Execution Slowdown" }`
2.  **Loads Definitions**: Reads from `backend/scenarios/definitions.json`.
3.  **Refactors Agents**:
    *   Agents must accept an optional `override_data` or `sim_mode=True` parameter.
    *   If present, the Agent **SKIPS** data fetching (GitHub/Greenhouse) and uses the override.
4.  **Runs Board Logic**: The `ExecutiveEvaluator` runs as normal, but consumes the *simulated* agent outputs.
5.  **Returns Result**: Labeled with `mode: "SIMULATION"`.

---

## 7. Board Reasoning Under Scenarios
The Board Agent does **not** know it is in a simulation. It reasons over the inputs provided.
*   **Example**: "Under this scenario, the execution signals (Declining) contradict the Narrative (Optimistic). This triggers the 'Execution Decay' risk pattern."

---

## 8. Frontend Design (Scenario Mode)
### UI Behavior
*   **Toggle**: `[ LIVE | SIMULATION ]` switch.
*   **Selector**: Dropdown to pick specific scenario.
*   **Banner**: clear "SIMULATION MODE - NOT REAL DATA" warning.

### Visual Rules
*   **Styling**: Muted colors or "Blueprint" aesthetic for Sim Mode.
*   **Borders**: Dashed border around the Risk Card.

### Storytelling
The UI must explicitly key off the differences:
*   *"If engineering slows by 35%, your Risk Level shifts from Low to **High**."*

---

## 9. Safeguards
1.  **No Writes**: Simulation runs must NOT be saved to `sqlite` history.
2.  **Isolation**: Simulation requests are ephemeral.
3.  **Transparency**: Every simulated API response includes a `simulation_metadata` block.

---

## 10. Implementation Plan
1.  **Backend**: Create `ScenarioController` and refactor Agents.
2.  **API**: expose `/api/board/simulate`.
3.  **Frontend**: Add toggle and state management for "Sim Mode".
