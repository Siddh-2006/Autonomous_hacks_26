# IF-THEN rules
def apply_rules(signals):
    """Apply business logic rules to agent signals"""
    rules_triggered = []
    
    # Rule 1: Material Execution Risk
    tech = signals.get("CTO", {})
    finance = signals.get("CFO", {})
    product = signals.get("CPO", {})
    
    if (tech.get("severity") == "high" and 
        finance.get("severity") == "medium" and
        product.get("severity") == "medium"):
        rules_triggered.append({
            "rule": "Material Execution Risk",
            "confidence": 0.85,
            "agents_involved": ["CTO", "CFO", "CPO"]
        })
    
    # Rule 2: Governance Risk
    risk = signals.get("RISK", {})
    if risk.get("urgency") == "High":
        rules_triggered.append({
            "rule": "Governance Alert",
            "confidence": 0.9,
            "agents_involved": ["RISK"]
        })
    
    return rules_triggered