# Agent scheduler
import json
import time
import sys
import os

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)).replace('scheduler', ''))

from agents.cto_agent import CTOAgent
from agents.cfo_agent import CFOAgent
from agents.ceo_agent import CEOAgent
from agents.cpo_agent import CPOAgent
from agents.risk_agent import RiskAgent
from reasoning.reasoning_engine import reason
from alerts.alert_engine import trigger_alert

def run_all_agents():
    """Run all agents and collect signals"""
    agents = [
        CTOAgent(),
        CFOAgent(),
        CEOAgent(),
        CPOAgent(),
        RiskAgent()
    ]
    
    signals = {}
    
    for agent in agents:
        try:
            # Fetch data
            data = agent.fetch_data()
            
            # Analyze data
            analysis = agent.analyze(data)
            
            # Emit signal
            signal = agent.emit_signal(analysis)
            signals[agent.name] = signal
            
            print(f"{agent.name} Agent: {analysis}")
            
        except Exception as e:
            print(f"Error running {agent.name} agent: {e}")
    
    # Store signals
    store_signals(signals)
    
    # Run reasoning
    reasoning_output = reason(signals)
    
    # Trigger alerts if needed
    if reasoning_output:
        trigger_alert(reasoning_output)
    
    return signals

def store_signals(signals):
    """Store latest signals"""
    try:
        # Get the correct path relative to backend directory
        storage_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "signals.json")
        with open(storage_path, "w") as f:
            json.dump({
                "latest_signals": signals,
                "last_updated": time.time()
            }, f, indent=2)
    except Exception as e:
        print(f"Error storing signals: {e}")

if __name__ == "__main__":
    print("Running all agents...")
    run_all_agents()