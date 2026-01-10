from apscheduler.schedulers.background import BackgroundScheduler
from run_cto_agent import run_cto_analysis
import atexit

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Run every 6 hours
    scheduler.add_job(func=run_cto_analysis, trigger="interval", hours=6)
    scheduler.start()
    
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
