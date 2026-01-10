from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys

sys.path.append("d:/Autonomous _hacks/auto-diligence")

from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot, init_db
from backend.reasoning.evaluator import ExecutiveEvaluator
# We might want to trigger runs via API too, but let's stick to reading first
from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent

app = FastAPI(title="Auto-Diligence Executive API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/board/status")
def get_board_status():
    """Get the latest Board Verdict and Agent Signals."""
    board_agent = ExecutiveReasoningAgent()
    # For a real dashboard, we might not want to RUN the agent on every page load (slow).
    # Instead, we should read the DB. But the user said "sees all that 4 agents checks... real time".
    # So we will trigger a run (or read latest if recent).
    # For demo purposes, we READ the latest DB state for speed, 
    # but provide a /refresh endpoint.
    
    # Actually, let's just run logic on latest snapshots to be fast.
    evaluator = ExecutiveEvaluator()
    verdict = evaluator.evaluate_current_state()
    
    # Fetch history for "Thesis Evolution"
    from backend.db.database import get_executive_history
    history = get_executive_history(limit=5)
    
    return {
        "verdict": verdict,
        "history": history,
        "agents": {
            "cfo": get_latest_cfo_snapshot(),
            "ceo": get_latest_ceo_snapshot(),
            "cto": get_latest_cto_snapshot()
        }
    }

@app.post("/api/board/refresh")
def refresh_board():
    """Force run all agents (Long polling)."""
    # 1. Run all agents (This is slow, 10s+)
    from backend.agents.cfo.agent import CFOAgent
    from backend.agents.ceo.agent import CEOAgent
    from backend.agents.cto.agent import CTOAgent
    
    CFOAgent().analyze()
    CEOAgent().analyze()
    CTOAgent().analyze()
    
    # 2. Run Board
    board_agent = ExecutiveReasoningAgent()
    result = board_agent.analyze()
    
    return {"status": "Refreshed", "result": result}
