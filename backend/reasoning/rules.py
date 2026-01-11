def evaluate_executive_risk(cfo_snapshot, cto_snapshot, ceo_snapshot, cpo_snapshot=None):
    """
    Board-Level Executive Reasoning Layer.
    Authoritative Rule Engine based on Master Spec.
    
    Inputs are final snapshots from C-Suite Agents.
    """
    
    # 1. Normalize Inputs (Handle missing/defaults)
    cfo_mode = cfo_snapshot.get('financial_mode', 'Stable')
    cto_health = cto_snapshot.get('execution_health', 'Stable')
    ceo_health = ceo_snapshot.get('narrative_health', 'Stable')
    cpo_health = cpo_snapshot.get('product_health', 'Healthy') if cpo_snapshot else 'Healthy'
    
    # Helper for "Negative" signals
    is_cto_bad = cto_health in ['Declining', 'Critical']
    is_cpo_bad = cpo_health in ['Declining', 'Stressed']
    is_ceo_good = ceo_health in ['Strong', 'Growth']
    is_cfo_tight = cfo_mode in ['Cost-Control', 'Distress']
    
    # 2. Risk Pattern Matching (The 5 Core Dimensions)
    
    # [3.4] TERMINAL RISK (The Death Spiral)
    # CTO Zombie + CFO Cutting + CPO Dying
    if is_cto_bad and is_cfo_tight and is_cpo_bad:
        return {
            'overall_risk': 'Critical',
            'risk_type': 'Terminal',
            'confidence': 0.95,
            'reason': "DEATH SPIRAL DETECTED: Engineering is stalled, Finance is cutting costs, and Product adoption is failing. Immediate intervention required."
        }

    # [3.3] PRODUCT-MARKET DISCONNECT (The Delusion)
    # CPO Declining + CEO Optimistic
    if is_cpo_bad and is_ceo_good:
        return {
            'overall_risk': 'Critical',
            'risk_type': 'Product',
            'confidence': 0.9,
            'reason': "REALITY GAP: CEO is selling a growth narrative while User Metrics (CPO) show decline. Strong PMF disconnect."
        }
        
    # [3.1] NARRATIVE INFLATION RISK
    # CEO Optimistic + CTO Declining
    if is_cto_bad and is_ceo_good:
        return {
            'overall_risk': 'High',
            'risk_type': 'Narrative',
            'confidence': 0.85,
            'reason': "EXECUTION GAP: Strategic narrative is bullish, but Engineering delivery is failing. High risk of missed roadmap."
        }

    # [3.2] EXECUTION DECAY RISK
    # CTO Declining + CFO Tightening
    if is_cto_bad and is_cfo_tight:
        return {
            'overall_risk': 'High',
            'risk_type': 'Execution',
            'confidence': 0.85,
            'reason': "OPERATIONAL STRESS: Engineering velocity is dropping while resources are being cut. Burnout/Churn risk is high."
        }

    # [3.4b] FINANCIAL MASKING (Modified)
    # CFO Tightening + CEO Growth
    if is_cfo_tight and is_ceo_good:
        return {
            'overall_risk': 'Medium',
            'risk_type': 'Financial',
            'confidence': 0.8,
            'reason': "MIXED SIGNALS: CEO promises growth while CFO executes cost-control. Potential 'Turnaround' or capital constraints."
        }

    # [3.5] THE GOLDEN PATH (Ideal)
    # Alignment of positives
    if not is_cto_bad and not is_cpo_bad and not is_cfo_tight:
        return {
            'overall_risk': 'Low',
            'risk_type': 'Growth',
            'confidence': 0.9,
            'reason': "GOLDEN PATH: Financials, Product, and Engineering are aligned for sustainable growth."
        }

    # DEFAULT: Mixed/Stable
    return {
        'overall_risk': 'Medium',
        'risk_type': 'Mixed',
        'confidence': 0.6,
        'reason': "STABLE: No critical contradictions detected, but signals are mixed. Monitor for trend changes."
    }