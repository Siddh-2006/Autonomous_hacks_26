import sqlite3
import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.database import get_db_connection
try:
    from backend.storage.vector_db import vector_memory
except ImportError:
    vector_memory = None

from backend.agents.ceo.agent import CEOAgent

def inspect_sqlite():
    print("\n=== 1. SQLite Database Inspection (Structured Data) ===")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    tables = ['cfo_snapshots', 'ceo_snapshots', 'cto_snapshots', 'executive_snapshots']
    
    for table in tables:
        try:
            # Get Row Count
            count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            
            # Get Columns
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]
            
            print(f"Table: {table.upper()}")
            print(f"  > Rows: {count}")
            print(f"  > Fields ({len(columns)}): {', '.join(columns)}")
            
            # Show latest entry sample
            if count > 0:
                latest = cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 1").fetchone()
                print(f"  > Latest Entry: {dict(latest)}")
            print("-" * 40)
            
        except sqlite3.OperationalError:
            print(f"Table: {table.upper()} (NOT FOUND - Schema Issue?)")
            
    conn.close()

def inspect_vectors():
    print("\n=== 2. Vector Database Inspection (Deep Memory) ===")
    if not vector_memory:
        print("Vector DB module not loaded.")
        return

    try:
        count = vector_memory.collection.count()
        print(f"Total Stored Narratives: {count}")
        
        # Peek at some metadata to see distribution
        peek = vector_memory.collection.peek(limit=5)
        if peek and peek['metadatas']:
            print("Sample Memories:")
            for meta in peek['metadatas']:
                print(f"  > Agent: {meta.get('agent')} | Type: {meta.get('type', 'N/A')} | Date: {meta.get('timestamp', 'N/A')}")
    except Exception as e:
        print(f"Vector Inspection Failed: {e}")

def benchmark_ceo():
    print("\n=== 3. CEO Agent Efficiency Benchmark ===")
    print("Running End-to-End CEO Analysis (News -> Context -> Vector Check -> Logic)...")
    
    start_time = time.time()
    
    agent = CEOAgent()
    result = agent.analyze()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n[SUCCESS] CEO Cycle Finished in {duration:.2f} seconds.")
    print(f"Status: {result.get('narrative_health')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Explanation: {result.get('explanation')}")

if __name__ == "__main__":
    print(f"Auto-Diligence System Audit - {datetime.now().isoformat()}")
    inspect_sqlite()
    inspect_vectors()
    benchmark_ceo()
    print("\n=== Audit Complete ===")
