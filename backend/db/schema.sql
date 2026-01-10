CREATE TABLE IF NOT EXISTS cfo_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    open_roles INTEGER,
    role_change_pct REAL,
    engineering_roles_pct REAL,
    sales_roles_pct REAL,
    ops_roles_pct REAL,
    financial_mode TEXT,
    severity TEXT,
    confidence REAL,
    explanation TEXT
);
