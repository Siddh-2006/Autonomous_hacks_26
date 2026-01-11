import sqlite3
import os
from datetime import datetime
import json

CFO_DB_PATH = os.path.join(os.path.dirname(__file__), 'cfo.db')
CTO_DB_PATH = os.path.join(os.path.dirname(__file__), 'cto_agent.db')

def get_db_connection():
    conn = sqlite3.connect(CFO_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

# --- CFO Functions ---
def insert_cfo_snapshot(data: dict):
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

def get_latest_cfo_snapshot():
    conn = get_db_connection()
    snapshot = conn.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp DESC LIMIT 1').fetchone()
    conn.close()
    if snapshot:
        return dict(snapshot)
    return None

def get_all_snapshots(): # Legacy/General
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- CEO Functions ---
def insert_ceo_snapshot(data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO ceo_snapshots (timestamp, narrative_health, severity, confidence, forward_looking_score, defensive_score, sentiment_trend, explanation, raw_signals)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        data['narrative_health'],
        data['severity'],
        data['confidence'],
        data['forward_looking_score'],
        data['defensive_score'],
        data['sentiment_trend'],
        data['explanation'],
        json.dumps(data.get('raw_signals', {}))
    ))
    conn.commit()
    conn.close()

def get_latest_ceo_snapshot():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ceo_snapshots ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_ceo_history(limit=5):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM ceo_snapshots ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- CTO Functions ---
def insert_cto_snapshot(data):
    conn = get_cto_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO cto_snapshots (
            timestamp, total_commits, commit_velocity_change_pct, 
            active_contributors, consistency_score, release_cadence, 
            core_repo_activity, bus_factor_risk, composite_health_score,
            execution_health, severity, confidence, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('timestamp', datetime.now().isoformat()),
        data.get('signals', {}).get('commit_velocity_change_pct', 0) * 2,  # Rough total commits approximation
        data.get('signals', {}).get('commit_velocity_change_pct', 0.0),
        data.get('signals', {}).get('active_contributors', 0),
        data.get('signals', {}).get('consistency_score', 0.0),
        data.get('signals', {}).get('release_cadence', 'unknown'),
        data.get('signals', {}).get('core_repo_activity', 'unknown'),
        data.get('signals', {}).get('bus_factor_risk', 'unknown'),
        data.get('signals', {}).get('composite_health_score', 0.0),
        data.get('execution_health', 'Stable'),
        data.get('severity', 'Low'),
        data.get('confidence', 0.0),
        data.get('explanation', '')
    ))
    conn.commit()
    conn.close()

def get_latest_cto_snapshot():
    conn = get_cto_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cto_snapshots ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_cto_snapshots():
    conn = get_cto_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cto_snapshots ORDER BY timestamp ASC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_cto_history(limit=5):
    conn = get_cto_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cto_snapshots ORDER BY timestamp DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_executive_history(limit=5):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        # Check if table exists first (handling legacy dbs)
        c.execute('SELECT * FROM executive_snapshots ORDER BY timestamp DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.OperationalError:
        return []
    finally:
        conn.close()


# --- CPO Functions ---
def insert_cpo_snapshot(data):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO cpo_snapshots (
            timestamp, product_health, severity, 
            adoption_trend, issue_pressure, maintainer_responsiveness,
            ecosystem_dependency, confidence, explanation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('timestamp', datetime.now().isoformat()),
        data.get('product_health'),
        data.get('severity'),
        data.get('signals', {}).get('adoption_trend'),
        data.get('signals', {}).get('issue_pressure'),
        data.get('signals', {}).get('maintainer_responsiveness'),
        data.get('signals', {}).get('ecosystem_dependency'),
        data.get('confidence'),
        data.get('explanation')
    ))
    conn.commit()
    conn.close()

def get_latest_cpo_snapshot():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cpo_snapshots ORDER BY timestamp DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
