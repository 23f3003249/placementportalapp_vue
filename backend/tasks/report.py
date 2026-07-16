from flask import render_template
from celery_app import celery
from datetime import datetime
from models import Drive, Application
import os

from tasks.email import send_email

@celery.task
def monthly_report():

    today = datetime.now()

    current_month_start = datetime(today.year,today.month,1)

    if today.month == 1:
        previous_month_start = datetime(today.year-1,12,1)

    else:
        previous_month_start = datetime(today.year,today.month-1,1)


    drives = Drive.query.filter(Drive.created_at >= previous_month_start, Drive.created_at < current_month_start).count()
    applications = Application.query.filter(Application.applied_at >= previous_month_start, Application.applied_at < current_month_start).count()
    selected = Application.query.filter(Application.status == "Selected", Application.status_updated_at >= previous_month_start, Application.status_updated_at < current_month_start).count()

    month_name = previous_month_start.strftime( "%B %Y")
    html = render_template("monthly_report.html",month=month_name, drives=drives, applications=applications, selected=selected)

    send_email(os.getenv("ADMIN_EMAIL"), f"Placement Activity Report - {month_name}", html)

    return {
        "month": month_name,
        "drives": drives,
        "applications": applications,
        "selected": selected
    }


monthly_report()