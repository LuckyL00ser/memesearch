import time
import schedule

from globals import ANALYZE_EVERY_N_MINUTES
from scan_analyze import analyze_memes
from logger import logger

schedule.every(ANALYZE_EVERY_N_MINUTES).minutes.do(analyze_memes) 

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    logger.info(f'Scheduler started every {ANALYZE_EVERY_N_MINUTES} minutes.')
    run_scheduler()