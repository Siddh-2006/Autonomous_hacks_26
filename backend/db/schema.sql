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
    raw_signals TEXT
);

CREATE TABLE IF NOT EXISTS cto_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    total_commits INTEGER,
    commit_velocity_change_pct REAL,
    active_contributors INTEGER,
    consistency_score REAL,
    release_cadence TEXT,
    core_repo_activity TEXT,
    bus_factor_risk TEXT,
    composite_health_score REAL,
    execution_health TEXT,
    severity TEXT,
    confidence REAL,
    explanation TEXT
);

CREATE TABLE IF NOT EXISTS executive_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    overall_risk TEXT,
    confidence REAL,
    summary TEXT,
    supporting_agents TEXT -- JSON
);
