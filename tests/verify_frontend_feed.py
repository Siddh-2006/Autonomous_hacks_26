import requests
import sys

def verify_frontend():
    print("--- FRONTEND DATA VERIFICATION ---")
    try:
        # Check if dashboard APi is up
        url = "http://127.0.0.1:8000/api/board/status"
        print(f"[TEST] Contacting API: {url}")
        
        resp = requests.get(url, timeout=5)
        
        if resp.status_code == 200:
            data = resp.json()
            verdict = data.get("verdict", {})
            agents = data.get("agents", {})
            
            print(f"[PASS] API is Live (Status: {resp.status_code})")
            print(f"[DATA] Board Verdict: {verdict.get('overall_risk')} ({verdict.get('confidence')*100:.0f}% confidence)")
            print(f"[DATA] CFO Mode: {agents.get('cfo', {}).get('financial_mode')}")
            print(f"[DATA] CEO Health: {agents.get('ceo', {}).get('health')}")
            
            # Check for Vector Evidence in the Payload
            # Ideally the frontend shows meaningful reasonings derived from Vectors
            cfo_exp = agents.get('cfo', {}).get('explanation', '')
            if "EARNINGS ALERT" in cfo_exp:
                 print("[PASS] Vector Intelligence (Evasion) present in API Payload.")
            else:
                 print("[INFO] No Earnings Alert in current snapshot (Might be clean).")
                 
            return True
        else:
            print(f"[FAIL] API Returned {resp.status_code}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Could not reach API: {e}")
        print("ensure 'python launch_dashboard.py' is running.")
        return False

if __name__ == "__main__":
    verify_frontend()
