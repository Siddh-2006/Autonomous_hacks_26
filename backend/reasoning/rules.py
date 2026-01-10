def evaluate_executive_risk(cfo_snapshot, cto_snapshot, ceo_snapshot):
    """
    Deterministic Rule Engine for Cross-Agent Executive Reasoning.
    
    Inputs:
        cfo_snapshot: {'financial_mode': 'Growth'|'Stable'|'Cost-Control', ...}
        cto_snapshot: {'execution_health': 'Strong'|'Stable'|'Declining', ...}
        ceo_snapshot: {'narrative_health': 'Strong'|'Stable'|'Weakening', ...}
        
    Returns:
        {
            'overall_risk': 'Low'|'Medium'|'High'|'Critical',
            'reason': "Executive summary string",
            'confidence': 0.0-1.0
        }
    """
    
    # 1. Extract Signals (with defaults)
    cfo_mode = cfo_snapshot.get('financial_mode', 'Stable')
    cto_health = cto_snapshot.get('execution_health', 'Stable')
    ceo_health = ceo_snapshot.get('narrative_health', 'Stable')
    
    # 2. Apply Deterministic Rules (Ordered by Severity)
    
    # CRITICAL RISK: Execution Collapse + Financial Distress
    if cto_health == 'Declining' and cfo_mode == 'Cost-Control':
        return {
            'overall_risk': 'Critical',
            'reason': "Double Negative: Engineering execution is declining while finance is cutting costs. High risk of product stagnation.",
            'confidence': 0.95
        }

    # HIGH RISK: The "Turnaround Trap" (Talking Growth, Acting Broke)
    if ceo_health == 'Strong' and cfo_mode == 'Cost-Control':
        return {
            'overall_risk': 'High',
            'reason': "Narrative Disconnect: CEO promises growth/innovation while CFO is actively cutting costs. 'Turnaround trap' detected.",
            'confidence': 0.9
        }

    # HIGH RISK: The "Vaporware Warning" (Hype without Code)
    if ceo_health == 'Strong' and cto_health == 'Declining':
        return {
            'overall_risk': 'High',
            'reason': "Execution Gap: Strategic narrative is bullish but engineering momentum is failing. Risk of missed delivery.",
            'confidence': 0.85
        }
        
    # MEDIUM RISK: Financial Tightening (Operational discipline?)
    if cfo_mode == 'Cost-Control' and cto_health == 'Stable':
        return {
            'overall_risk': 'Medium',
            'reason': "Financial tightening detected. Engineering is resilient so far, but monitor for burnout/churn.",
            'confidence': 0.8
        }

    # MEDIUM RISK: Leadership Doubts
    if ceo_health == 'Weakening' and cfo_mode == 'Growth':
        return {
            'overall_risk': 'Medium',
            'reason': "Leadership confidence is wavering despite financial expansion. Potential internal strategy pivoting.",
            'confidence': 0.75
        }

    # LOW RISK: The "Golden Path"
    if cfo_mode == 'Growth' and cto_health == 'Strong':
        return {
            'overall_risk': 'Low',
            'reason': "Ideal State: Financial resources are fueling strong engineering execution.",
            'confidence': 0.9
        }

    # DEFAULT: Stable/Mixed
    return {
        'overall_risk': 'Low',
        'reason': "No material cross-agent conflicts detected. Operations appear aligned.",
        'confidence': 0.6
    }