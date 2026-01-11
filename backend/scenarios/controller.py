import json
import os
from copy import deepcopy
from backend.reasoning.evaluator import ExecutiveEvaluator
from backend.db.database import get_latest_cfo_snapshot, get_latest_ceo_snapshot, get_latest_cto_snapshot, get_latest_cpo_snapshot

class ScenarioController:
    def __init__(self):
        # Load definitions
        definition_path = os.path.join(os.path.dirname(__file__), 'definitions.json')
        with open(definition_path, 'r') as f:
            data = json.load(f)
            self.scenarios = {s['id']: s for s in data['scenarios']}

    def get_available_scenarios(self):
        """Return list of scenarios for UI."""
        return [
            {"id": k, "name": v['name'], "description": v['description']} 
            for k, v in self.scenarios.items()
        ]

    def run_simulation(self, scenario_id):
        """Run the Board Logic under specific stress conditions."""
        if scenario_id not in self.scenarios:
            raise ValueError(f"Unknown scenario: {scenario_id}")

        scenario = self.scenarios[scenario_id]
        overrides = scenario.get('overrides', {})

        # 1. Fetch Real Baseline Data
        # We start with reality, then twist it.
        cfo = get_latest_cfo_snapshot() or {"financial_mode": "Stable", "explanation": "No Data"}
        ceo = get_latest_ceo_snapshot() or {"narrative_health": "Stable", "explanation": "No Data"}
        cto = get_latest_cto_snapshot() or {"execution_health": "Healthy", "explanation": "No Data"}
        cpo = get_latest_cpo_snapshot() or {"product_health": "Healthy", "explanation": "No Data"}
        
        # 2. Apply Overrides
        # We use deepcopy to ensure we don't accidentally mutate any cached objects
        agents = {
            'cfo': deepcopy(cfo),
            'ceo': deepcopy(ceo),
            'cto': deepcopy(cto),
            'cpo': deepcopy(cpo)
        }

        for agent_name, patch in overrides.items():
            if agent_name in agents and patch:
                agents[agent_name].update(patch)

        # 3. Run Board Logic (Evaluator)
        # We need to inject these strictly into the evaluator
        evaluator = ExecutiveEvaluator()
        
        # We need to modify evaluator to accept direct inputs, or pass them to the rules function directly
        # Since evaluator.evaluate_current_state() internally fetches data, we should refactor it
        # Or here, we can just use the rules engine directly since the Evaluator is just a wrapper.
        # However, to keep "Memory" logic consistent, we should use the Evaluator if possible.
        # Let's assume we refactor Evaluator to accept 'manual_snapshots'.
        
        verdict = evaluator.evaluate_current_state(manual_snapshots=agents)
        
        # 4. Tag Result
        verdict['mode'] = 'SIMULATION'
        verdict['scenario'] = scenario['name']
        verdict['summary'] = f"[SIMULATION: {scenario['name']}] {verdict['summary']}"
        
        return {
            "verdict": verdict,
            "agents": agents,
            "scenario": scenario
        }
