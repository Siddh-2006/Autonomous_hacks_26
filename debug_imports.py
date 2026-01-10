import sys
import os

sys.path.append("d:/Autonomous _hacks/auto-diligence")

try:
    print("Attempting to import database...")
    from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot
    print("Database functions imported successfully.")
except ImportError as e:
    print(f"Database Import Failed: {e}")
except Exception as e:
    print(f"Database Error: {e}")

try:
    print("Attempting to import Evaluator...")
    from backend.reasoning.evaluator import ExecutiveEvaluator
    print("Evaluator imported successfully.")
except ImportError as e:
    print(f"Evaluator Import Failed: {e}")
