# Auto-Diligence System

Autonomous Agent-Based Investor Due Diligence & Monitoring System

## Overview

This system continuously evaluates a company's health from the perspective of its executive leadership (CEO, CTO, CFO, CPO, and Board) using only publicly available data.

## Architecture

### Backend (Python/FastAPI)
- **Agents**: Specialized agents for each executive perspective
  - CEO Agent: Strategy & narrative analysis
  - CTO Agent: Technology & execution monitoring
  - CFO Agent: Financial discipline & cost signals
  - CPO Agent: Product & user reality
  - Risk Agent: Governance & legal risks

- **Reasoning Engine**: Cross-agent logic and alert generation
- **Data Sources**: GitHub, news, hiring, product signals
- **Storage**: JSON-based signal storage with optional vector memory

### Frontend (React)
- Real-time dashboard showing agent status
- Alert notifications
- Timeline of events
- Current investment thesis

## Quick Start

### Backend Setup
```bash
cd backend
pip install -r ../requirements.txt
python scheduler/run_agents.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

### Run Demo
```bash
python scripts/simulate_change.py
```

## Key Features

- **Autonomous Monitoring**: Agents run continuously without human intervention
- **Executive Perspective**: Each agent thinks like a senior executive
- **Explainable Alerts**: Clear reasoning for why alerts are triggered
- **Memory**: Historical context for better decision making
- **Single Critical Alert**: "Material Execution Risk" to avoid alert fatigue

## File Structure

```
auto-diligence/
├── backend/
│   ├── agents/          # Executive perspective agents
│   ├── reasoning/       # Cross-agent logic
│   ├── data_sources/    # Data collection modules
│   ├── storage/         # Signal and history storage
│   ├── alerts/          # Alert generation
│   └── scheduler/       # Agent orchestration
├── frontend/
│   └── src/            # React dashboard components
└── scripts/            # Demo and utility scripts
```

## Philosophy

This system automates what institutional investors already do manually:
- Continuous due diligence
- Risk monitoring  
- Thesis validation

It behaves like a permanent analyst team that never sleeps, never forgets history, and never relies on gut feeling.