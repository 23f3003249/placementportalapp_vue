from database import db
from datetime import datetime


class User( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))
    approved = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    student = db.relationship('Student', backref='user', uselist=False)
    company = db.relationship('Company', backref='user', uselist=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    resume = db.Column(db.String(200), nullable=True)
    applications = db.relationship('Application', backref='student', lazy=True)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    website = db.Column(db.String(100), nullable=True)
    hr_email = db.Column(db.String(100),unique=True, nullable=False)
    drives =  db.relationship('Drive', backref='company', lazy=True)


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'),nullable=False)
    status = db.Column(db.String(50), default="Applied")
    applied_at = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    status_updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    interview_date = db.Column(db.String(20),nullable=True)
    interview_link = db.Column(db.String(150),nullable=True)
    __table_args__ = (db.UniqueConstraint("student_id","drive_id",name="uq_student_drive"),
)
    


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)