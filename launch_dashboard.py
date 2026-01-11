import uvicorn
import os
import sys

if __name__ == "__main__":
    print("Starting Auto-Diligence Dashboard API...")
    print("Once running, access the dashboard at: http://127.0.0.1:8000")
    uvicorn.run("backend.api.main:app", host="127.0.0.1", port=8000, reload=True)
