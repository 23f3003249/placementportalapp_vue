from celery import Celery
import os
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

#celery instance 
from app import create_app

app = create_app()

#redis config 
celery = Celery("placementportal",broker=os.getenv("REDIS_BROKER_URL"),backend=os.getenv("REDIS_BACKEND_URL"),
               include=["tasks.reminder","tasks.report","tasks.export"])

celery.conf.update(timezone="Asia/Kolkata", enable_utc=False)

#beat schedule 
celery.conf.beat_schedule = {
    "daily-placement-remainder":{
        "task":"tasks.reminder.daily_reminder",
        "schedule":crontab(hour=9,minute=0),
    },
    "monthly-placement-report":{
        "task":"tasks.report.monthly_report",
        "schedule":crontab(day_of_month=1,hour=9,minute=0)

    }
}

#Flask context integration
class FlaskTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        
celery.Task = FlaskTask
