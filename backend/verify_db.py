from backend.db.database import get_all_snapshots
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    snapshots = get_all_snapshots()
    print(f"Found {len(snapshots)} snapshots.")
    for s in snapshots:
        print(s)
except Exception as e:
    print(e)
