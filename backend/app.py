# FastAPI entry point
from fastapi import FastAPI

app = FastAPI(title="Auto-Diligence System")

@app.get("/")
def read_root():
    return {"message": "Auto-Diligence System API"}