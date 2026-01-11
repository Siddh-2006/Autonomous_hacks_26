from datetime import datetime

class ChangeDetector:
    def __init__(self):
        self.risk_ordering = {'Low': 0, 'Medium': 1, 'High': 2, 'Critical': 3}

    def detect_changes(self, current_verdict, previous_verdict):
        """
        Compare two verdicts and determine if an ALERT is necessary.
        Returns: Alert Dict or None
        """
        if not previous_verdict:
            return None # No history to compare
            
        alert = None
        timestamp = current_verdict.get('timestamp', datetime.now().isoformat())
        
        # 1. Check Risk Level Jump (e.g. Low -> High)
        curr_risk = current_verdict.get('overall_risk', 'Medium')
        prev_risk = previous_verdict.get('overall_risk', 'Medium')
        
        curr_score = self.risk_ordering.get(curr_risk, 1)
        prev_score = self.risk_ordering.get(prev_risk, 1)
        
        # JUMP UP (Worsening)
        if curr_score > prev_score:
            severity = "WARNING"
            if curr_score >= 3: # Critical
                severity = "CRITICAL"
                
            alert = {
                "alert_type": severity,
                "reason": f"Risk Level escalated from {prev_risk} to {curr_risk}.",
                "change_type": "RISK_ESCALATION",
                "previous": prev_risk,
                "current": curr_risk
            }

        # 2. Check Risk Type Pivot (e.g. Execution -> Product)
        # Only if risk is at least Medium, otherwise noise.
        elif curr_score >= 1 and current_verdict.get('risk_type') != previous_verdict.get('risk_type'):
            alert = {
                "alert_type": "INFO", # Info only unless it's a critical type
                "reason": f"Risk Thesis pivoted from {previous_verdict.get('risk_type')} to {current_verdict.get('risk_type')}.",
                "change_type": "THESIS_PIVOT",
                "previous": previous_verdict.get('risk_type'),
                "current": current_verdict.get('risk_type')
            }
            
        # 3. Check Confidence Collapse (Optional - if needed)
        # ...
        
        if alert:
            alert['timestamp'] = timestamp
            alert['conf_score'] = current_verdict.get('confidence', 0)
            
        return alert
