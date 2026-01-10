import sys
import os

# Add project root to path
sys.path.append("d:/Autonomous _hacks/auto-diligence")

from backend.data_sources.careers_scraper import fetch_open_roles, fetch_latest_press_release

print("[TEST] Testing CFO Scraper (Live Only)...")
roles = fetch_open_roles()
print(f"Roles Found: {len(roles)}")
if roles:
    print("Sample:", roles[:3])
else:
    print("Result: EMPTY (Blocked or No Data)")

pr_text = fetch_latest_press_release()
print(f"PR Text Length: {len(pr_text)}")
if len(pr_text) == 0:
    print("Result: EMPTY (PR Fetch Not Implemented/Failed)")
