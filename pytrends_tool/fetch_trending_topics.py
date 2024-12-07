# pytrends_tool/fetch_trending_topics.py

import schedule
import time
from pytrends_lib.trends_integration import fetch_trending_topics

def job():
    fetch_trending_topics()

def main():
    # Schedule the job every 24 hours
    schedule.every(24).hours.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()