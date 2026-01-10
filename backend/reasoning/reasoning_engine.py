# Cross-agent logic
def reason(signals):
    tech = signals.get("CTO")
    finance = signals.get("CFO")
    
    if tech and finance:
        if tech.get("severity") == "high" and finance.get("severity") == "medium":
            return {
                "alert": "Material Execution Risk",
                "confidence_drop": 0.25
            }
    
    return None