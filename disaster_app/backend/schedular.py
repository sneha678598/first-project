import time
import sys
import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from src.idms_functions import fetch_live_data

# Add the parent directory to the system path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
# Add the parent directory of 'src' to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

# Print sys.path for debugging
print("Current sys.path:", sys.path)

# Setup loggingcd 
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

def fetch_data_periodically():
    logging.info("Fetching live data...")
    fetch_live_data(api_url=os.getenv("YOUR_API_URL"), save_file_name="data/live_data/live_data.json")

# Setup scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_data_periodically, 'interval', minutes=30)  # For testing every 30 minutes

scheduler.start()

logging.info("Scheduler started")

try:
    while True:
        time.sleep(1)  # Keep the script running
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    logging.info("Scheduler stopped")

