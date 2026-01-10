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

CREATE TABLE IF NOT EXISTS ceo_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    narrative_health TEXT NOT NULL,
    severity TEXT NOT NULL,
    confidence REAL NOT NULL,
    forward_looking_score REAL NOT NULL,
    defensive_score REAL NOT NULL,
    sentiment_trend TEXT NOT NULL,
    explanation TEXT,
    raw_signals TEXT -- JSON string for detailed signals
);

