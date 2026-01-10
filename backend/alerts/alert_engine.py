# Alert engine
import json
import time
import os

def trigger_alert(reasoning_output):
    """Trigger alert based on reasoning output"""
    if reasoning_output:
        alert = {
            "timestamp": time.time(),
            "alert_type": reasoning_output["alert"],
            "confidence": reasoning_output.get("confidence_drop", 0),
            "message": f"🚨 ALERT: {reasoning_output['alert']}"
        }
        
        # Store alert
        store_alert(alert)
        
        # Print to console (in production, would send to dashboard/notifications)
        print(f"🚨 ALERT: {reasoning_output['alert']}")
        
        return alert
    
    return None

def store_alert(alert):
    """Store alert in history"""
    try:
        # Get the correct path relative to backend directory
        history_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "history.json")
        
        with open(history_path, "r") as f:
            history = json.load(f)
        
        history["alert_history"].append(alert)
        
        with open(history_path, "w") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error storing alert: {e}")