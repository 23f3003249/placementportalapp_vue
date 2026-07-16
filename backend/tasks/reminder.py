from datetime import date , timedelta

from celery_app import celery
from database import db

from models import User, Drive, Student, Application

from tasks.email import send_email


@celery.task
def daily_reminder():

    tommorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    drives = Drive.query.filter_by(status= "Approved").all()
    students = Student.query.all()

    for ds in drives:
        if ds.deadline != tommorrow:
            continue

        for student in students:

            already_applied = Application.query.filter_by(student_id=student.id,drive_id=ds.id).first()
            if already_applied:
                continue
            if (ds.branch.lower() != "all" and ds.branch.lower() != student.branch.lower()):
                continue

            if student.cgpa < ds.cgpa: 
                continue
            if student.year != ds.year:
                continue
            user = db.session.get(User, student.user_id)

            if user is None or not user.active:
                continue

            html = f"""
<h2>Placement Drive Reminder</h2>
<h5>Hello, {user.name}</h5>
<p>Your application deadline for the <b>{ds.title}</b> is tommorrow, {ds.deadline}</p>
<p>Log in to your account to apply</p>
<button>Log in</button> """
                

            send_email(user.email, "Placement Drive Reminder", html)

