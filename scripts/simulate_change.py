# Demo simulation script
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from scheduler.run_agents import run_all_agents
import time

def simulate_company_decline():
    """Simulate a company going through execution challenges"""
    print("=== SIMULATION: Company Execution Decline ===")
    print("Simulating real-time monitoring of company health...")
    print()
    
    # Run agents multiple times to show progression
    for i in range(3):
        print(f"--- Monitoring Cycle {i+1} ---")
        signals = run_all_agents()
        print()
        
        if i < 2:
            print("Waiting 5 seconds for next cycle...")
            time.sleep(5)
    
    print("=== SIMULATION COMPLETE ===")
    print("Check the dashboard to see the results!")

if __name__ == "__main__":
    simulate_company_decline()