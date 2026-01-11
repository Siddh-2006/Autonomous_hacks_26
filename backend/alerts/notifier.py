import json

class Notifier:
    def __init__(self):
        # In production, we would hook up Slack/Email/PagerDuty here
        pass

    def send_alert(self, alert):
        """
        Dispatch the alert to configured channels.
        For now, we log to a file and print strictly.
        """
        if not alert:
            return

        # 1. Format Message
        emoji = "ℹ️"
        if alert['alert_type'] == 'WARNING': emoji = "⚠️"
        if alert['alert_type'] == 'CRITICAL': emoji = "🚨"
        
        msg = f"[{emoji} {alert['alert_type']}] {alert['reason']} ({alert.get('timestamp')})"
        
        # 2. "Send" (Print to console / Log)
        print(f"\n>>> ALERT DISPATCHED: {msg}\n")
        
        # 3. Log to file (Simulating persistence)
        # We append to an alerts.jsonl
        try:
            with open('backend/db/alerts.jsonl', 'a') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            print(f"Failed to log alert: {e}")
