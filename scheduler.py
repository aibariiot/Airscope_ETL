from apscheduler.schedulers.blocking import BlockingScheduler
from etl import run_etl
from datetime import datetime

def scheduled_job():
    result = run_etl()
    print(f"[{datetime.now()}] {result}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_job, "interval", minutes=15)
    print("Scheduler started. Running ETL every 15 minutes...")
    scheduled_job()  # run once immediately
    scheduler.start()
