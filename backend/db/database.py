import sqlite3
import os
from datetime import datetime

CFO_DB_PATH = os.path.join(os.path.dirname(__file__), 'cfo.db')
CTO_DB_PATH = os.path.join(os.path.dirname(__file__), 'cto_agent.db')

def get_cfo_db_connection():
    conn = sqlite3.connect(CFO_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_cto_db_connection():
    conn = sqlite3.connect(CTO_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Initialize CFO database
    conn = get_cfo_db_connection()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    
    # Initialize CTO database
    conn = get_cto_db_connection()
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# CFO Functions (existing)
def insert_cfo_snapshot(data: dict):
    conn = get_cfo_db_connection()
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

def get_latest_cfo_snapshot():
    conn = get_cfo_db_connection()
    snapshot = conn.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if snapshot:
        return dict(snapshot)
    return None

def get_all_cfo_snapshots():
    conn = get_cfo_db_connection()
    snapshots = conn.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp ASC').fetchall()
    conn.close()
    return [dict(row) for row in snapshots]

# CTO Functions (new)
def insert_cto_snapshot(data: dict):
    conn = get_cto_db_connection()
    conn.execute('''
        INSERT INTO cto_snapshots (
            timestamp, total_commits, commit_velocity_change_pct,
            active_contributors, consistency_score, release_cadence,
            core_repo_activity, execution_health, severity, confidence, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('timestamp'),
        data.get('signals', {}).get('commit_velocity_change_pct', 0) + data.get('signals', {}).get('commit_velocity_change_pct', 0),  # total commits approximation
        data.get('signals', {}).get('commit_velocity_change_pct'),
        data.get('signals', {}).get('active_contributors'),
        data.get('signals', {}).get('consistency_score'),
        data.get('signals', {}).get('release_cadence'),
        data.get('signals', {}).get('core_repo_activity'),
        data.get('execution_health'),
        data.get('severity'),
        data.get('confidence'),
        data.get('explanation')
    ))
    conn.commit()
    conn.close()

def get_latest_cto_snapshot():
    conn = get_cto_db_connection()
    snapshot = conn.execute('SELECT * FROM cto_snapshots ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if snapshot:
        return dict(snapshot)
    return None

def get_all_cto_snapshots():
    conn = get_cto_db_connection()
    snapshots = conn.execute('SELECT * FROM cto_snapshots ORDER BY timestamp ASC').fetchall()
    conn.close()
    return [dict(row) for row in snapshots]

# Legacy functions for backward compatibility
def get_db_connection():
    return get_cfo_db_connection()

def insert_snapshot(data: dict):
    return insert_cfo_snapshot(data)

def get_latest_snapshot():
    return get_latest_cfo_snapshot()

def get_all_snapshots():
    return get_all_cfo_snapshots()

# Initialize on module load or manually
if __name__ == "__main__":
    init_db()
    print("Databases initialized.")
