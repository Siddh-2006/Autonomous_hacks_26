# 🧠 Auto-Diligence: The Autonomous Executive Board

> **"Wall Street Intelligence in a Box"**
> An autonomous multi-agent system that audits companies like a Forensic Accountant, strategizes like a CEO, and reviews code like a CTO.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Production](https://img.shields.io/badge/Status-Production-green)](https://railway.app)
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

---

## 🚨 The The Problem: "Diligence is Broken"
In today's market, "Truth" is fragmented.
*   **Narrative vs. Reality Gap**: Executives say "We are investing for growth", but silently freeze hiring or stop shipping code.
*   **High Latency**: Quarterly earnings happen every 90 days. **Strategy breaks weeks before the numbers do.**
*   **Blindspots**: Financial analysts don't read GitHub commit logs.

## ⚡ The Solution: 4 Autonomous Executive Agents
We built **Job-Specific Agents** that live on the internet, wake up autonomously, and perform rigorous professional work 24/7.

| Agent | Role | Source of Truth | Core Question |
| :--- | :--- | :--- | :--- |
| **🕵️‍♂️ CFO Agent** | **Forensic Auditor** | **Greenhouse / Earnings Q&A** | "Is the company cutting costs while claiming growth? Is management evading questions?" |
| **♟️ CEO Agent** | **Strategic Sentinel** | **Google News / SEC Filings** | "Is the strategic narrative becoming defensive? Is there 'Strategy Drift' from 2 years ago?" |
| **👨‍💻 CTO Agent** | **Tech Auditor** | **GitHub API** | "Is engineering velocity slowing? Is there a 'Bus Factor' risk (knowledge silo)?" |
| **⚖️ CPO Agent** | **Product Auditor** | **GitHub Issues / App Store** | "Is the product actually working? Is there a gap between Marketing Hype and User Reality?" |

---

## 📚 Documentation (Deep Dives)
Each agent is a complex system. Read their "Brain" logic here:
*   [**👉 CFO Agent Guide**](docs/CFO_AGENT_EXPLAINED.md) (Forensics & Evasion Detection)
*   [**👉 CEO Agent Guide**](docs/CEO_AGENT_EXPLAINED.md) (Strategy Drift & Vectors)
*   [**👉 Board Agent Spec**](docs/BOARD_AGENT_MASTER_SPEC.md) (The 5 Core Risk Patterns)
*   [**👉 Dashboard UX Spec**](docs/DASHBOARD_UX_SPEC.md) (The "Dark/Elite" Design System)

---

## 🏗️ System Architecture (Vector-Enhanced)

This system uses a **Hybrid Architecture** (SQL + Vector) to remember the past and detecting anomalies.

```mermaid
graph TD
    subgraph "Tier 1: Sensors"
        Internet((Internet))
        Greenhouse[Careers Page]
        GNews[Google News]
        GitHub[GitHub API]
    end

    subgraph "Tier 2: The Executive Board (Agents)"
        CFO[👮 CFO Agent]
        CEO[🧠 CEO Agent]
        CTO[👨‍💻 CTO Agent]
        CPO[⚖️ CPO Agent]
        
        Greenhouse --> CFO
        GNews --> CEO
        GitHub --> CTO
        GitHub --> CPO
    end

    subgraph "Tier 3: The Brain (Memory)"
        SQL[(SQLite History)]
        Vector[(ChromaDB Semantic Memory)]
        
        CFO -->|Evasion Checks| Vector
        CEO -->|Strategy Baseline| Vector
        
        CFO -->|Snapshots| SQL
        CTO -->|Snapshots| SQL
        CPO -->|Snapshots| SQL
    end

    subgraph "Tier 4: The Experience"
        Dashboard[📊 "Elite" Terminal Dashboard]
        API[⚡ FastAPI Backend]
        
        SQL --> API
        API --> Dashboard
    end

    subgraph "Tier 5: Automation & Alerts (Background)"
        Cron[⏰ Cron Runner]
        Detector[⚠️ Change Detector]
        Notifier[🔔 Alert Dispatcher]
        
        Cron --> API
        API --> Detector
        Detector --> Notifier
    end
```

## 🚀 Quick Start (Running Locally)

### 1. Install & Run
```bash
# Install Dependencies
pip install -r requirements.txt

# Run the Full Board (Scheduler)
python backend/scheduler/run_agents.py
```

### 2. View the Dashboard
```bash
# Launch the API
python launch_dashboard.py
```
Open `frontend/index.html` in your browser.

## ☁️ Deployment (Railway)
This system is designed for **Persistent Cloud** deployment (Railway/Render).
It includes an **Auto-Backfill Hook**:
*   On first deploy, it automatically downloads 2 years of historical data into the Vector DB.
*   It seeds the "Thesis Timeline" so your dashboard looks populated instantly.

See [Deployment Cheat Sheet](docs/DEPLOYMENT_CHEAT_SHEET.md).