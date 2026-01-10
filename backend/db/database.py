import sqlite3
import os
from datetime import datetime
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'cfo.db')

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

def get_all_snapshots():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM cfo_snapshots ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

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

# Initialize on module load or manually
if __name__ == "__main__":
    init_db()
    print("Databases initialized.")
