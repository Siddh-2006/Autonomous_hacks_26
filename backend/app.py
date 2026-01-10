# FastAPI entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(__file__))

from agents.cto_agent import CTOAgent
from db.database import insert_cto_snapshot, get_latest_cto_snapshot, get_all_cto_snapshots, init_db

app = FastAPI(title="Auto-Diligence System")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Auto-Diligence System API"}

@app.get("/api/cto/latest")
def get_latest_cto_snapshot_api():
    """Get the latest CTO agent snapshot from database"""
    try:
        snapshot = get_latest_cto_snapshot()
        if snapshot:
            return snapshot
        else:
            # If no snapshot in DB, run agent and return result
            cto = CTOAgent()
            data = cto.fetch_data()
            analysis = cto.analyze(data)
            result = cto.emit_signal(analysis)
            return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/cto/history")
def get_cto_history():
    """Get CTO agent history from database"""
    try:
        snapshots = get_all_cto_snapshots()
        return {"snapshots": snapshots, "count": len(snapshots)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/cto/run")
def run_cto_agent():
    """Manually trigger CTO agent run and store in database"""
    try:
        cto = CTOAgent()
        data = cto.fetch_data()
        analysis = cto.analyze(data)
        result = cto.emit_signal(analysis)
        
        # Store in database
        insert_cto_snapshot(result)
        
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}