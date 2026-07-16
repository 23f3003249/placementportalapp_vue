import csv 
import os 

from celery_app import celery
from database import db
from models import Drive, Student, User, Application, Company

from tasks.email import send_email

@celery.task
def export_applications(student_id):

    student = db.session.get(Student, student_id)

    if not student:
        return 
    
    user = db.session.get(User, student.user_id)

    export_folder = "exports"

    os.makedirs(export_folder, exist_ok=True)
    filename = os.path.join(export_folder, f"{student.id}_applications.csv")
    applications = Application.query.filter_by(student_id=student.id).all()

    with open(filename, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["Student ID", "Student Name","Company" ,"Drive Title", "Application Status", "Applied At"])

            for application in applications:
                drive = db.session.get(Drive, application.drive_id)
                company = db.session.get(Company, drive.company_id)

                writer.writerow([
                student.id,
                user.name,
                company.company_name,
                drive.title,
                application.status,
                application.applied_at.strftime("%d-%m-%Y"),

            ])
           

    send_email(
            user.email,
        "Application Export Completed",
        """<html>
        <h2>Export Completed</h2><p>
            Your placement application
            history CSV has been generated.
        </p>
        <p>
        CSV report has been attached to this email.
        </p>
        <html>""",attachment=filename)
    return filename
    

        
        