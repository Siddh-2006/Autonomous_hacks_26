from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import sys


# sys.path.append("d:/Autonomous _hacks/auto-diligence") # Removed for Cloud Compatibility

from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot, get_latest_cpo_snapshot, init_db
from backend.reasoning.evaluator import ExecutiveEvaluator
# We might want to trigger runs via API too, but let's stick to reading first
from backend.agents.executive_reasoning_agent import ExecutiveReasoningAgent
from backend.scenarios.controller import ScenarioController
from pydantic import BaseModel

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimulationRequest(BaseModel):
    scenario_id: str

@app.get("/api/scenarios")
def list_scenarios():
    """Get available simulation scenarios."""
    controller = ScenarioController()
    return controller.get_available_scenarios()

@app.post("/api/board/simulate")
def run_simulation(req: SimulationRequest):
    """Run a specific simulation scenario."""
    try:
        controller = ScenarioController()
        return controller.run_simulation(req.scenario_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# --- SERVE FRONTEND (STATIC FILES) ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount the 'frontend' directory to serve CSS/JS if needed, or just the index
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

@app.on_event("startup")
def startup():
    init_db()
    
    # --- AUTO-DEPLOYMENT: VECTOR DB ---
    # Check if we need to hydrate the "Brain" (First run on Cloud)
    # --- AUTO-DEPLOYMENT: BACKGROUND SEEDING ---
    # We move this to a background thread so the API boots INSTANTLY.
    # Otherwise, Railway might time out (502 Error) waiting for the backfill to finish.
    def seed_data_background():
        import time
        time.sleep(2) # Give boot a moment
        from backend.storage.vector_db import vector_memory
        try:
            count = vector_memory.collection.count()
            print(f"[STARTUP] Vector Memory Count: {count}")
            if count < 5:
                print("[STARTUP] Fresh deployment detected. Auto-seeding Vector DB...")
                
                # 1. Backfill CEO Strategy (2 Years)
                from backend.vectors.backfill import run_backfill
                run_backfill()
                
                # 2. Seed CFO Risk Archetypes
                from backend.storage.seed_archetypes import seed_risk_archetypes
                seed_risk_archetypes()
                
                # 3. Seed SQLite History (Timeline)
                from backend.db.seed_history import seed_executive_history
                seed_executive_history()
                
                print("[STARTUP] Seeding Complete. System is ready.")
        except Exception as e:
            print(f"[STARTUP] Warning: Vector DB check failed: {e}")

    import threading
    seed_thread = threading.Thread(target=seed_data_background, daemon=True)
    seed_thread.start()

    # --- AUTO-DEPLOYMENT: SCHEDULER (The Heartbeat) ---
    # Start the 6-hour loop in a background thread so it runs alongside the API
    
    from backend.scheduler.run_agents import run_pipeline
    import schedule
    import time

    def scheduler_loop():
        print("[SCHEDULER] Background thread started.")
        # Run once immediately
        try:
            run_pipeline()
        except Exception as e:
            print(f"[SCHEDULER] Initial run failed: {e}")
            
        schedule.every(6).hours.do(run_pipeline)
        while True:
            schedule.run_pending()
            time.sleep(60)

    # Daemon thread dies when main app dies
    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()
    print("[STARTUP] Scheduler thread launched.")

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
            "cto": get_latest_cto_snapshot(),
            "cpo": get_latest_cpo_snapshot()
        }
    }

@app.post("/api/board/refresh")
def refresh_board():
    """Force run all agents (Long polling)."""
    # 1. Run all agents (This is slow, 10s+)
    from backend.agents.cfo.agent import CFOAgent
    from backend.agents.ceo.agent import CEOAgent
    from backend.agents.cto.agent import CTOAgent
    from backend.agents.cpo.agent import CPOAgent
    
    CFOAgent().analyze()
    CEOAgent().analyze()
    CTOAgent().analyze()
    CPOAgent().analyze()
    
    # 2. Run Board
    board_agent = ExecutiveReasoningAgent()
    result = board_agent.analyze()
    
    return {"status": "Refreshed", "result": result}
