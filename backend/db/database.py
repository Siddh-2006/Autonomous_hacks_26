import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'cfo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def insert_snapshot(data: dict):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO cfo_snapshots (
            timestamp, open_roles, role_change_pct, 
            engineering_roles_pct, sales_roles_pct, ops_roles_pct,
            financial_mode, severity, confidence, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('timestamp', datetime.now().isoformat()),
        data.get('open_roles'),
        data.get('role_change_pct'),
        data.get('engineering_roles_pct'),
        data.get('sales_roles_pct'),
        data.get('ops_roles_pct'),
        data.get('financial_mode'),
        data.get('severity'),
        data.get('confidence'),
        data.get('explanation')
    ))
    conn.commit()
    conn.close()

def get_latest_snapshot():
    conn = get_db_connection()
    snapshot = conn.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if snapshot:
        return dict(snapshot)
    return None

def get_all_snapshots():
    conn = get_db_connection()
    snapshots = conn.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp ASC').fetchall()
    conn.close()
    return [dict(row) for row in snapshots]

# Initialize on module load or manually
if __name__ == "__main__":
    init_db()
    print("Database initialized.")
