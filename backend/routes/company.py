from flask import Blueprint, request, jsonify, session
from database import db
from models import User, Student, Company, Drive, Application , Branch
from datetime import datetime

from auth_utils import role_required

company = Blueprint('company',__name__)

#company dashboardf
@company.route('/dashboard', methods=['GET'])
@role_required("company")
def company_dashboard():
    
    user = db.session.get(User, session['user_id'])
    company = Company.query.filter_by(user_id=user.id).first()

    drives = Drive.query.filter_by(company_id=company.id).all()

    applicants = sum(
        Application.query.filter_by(drive_id=d.id).count()
        for d in drives )

    return jsonify({
        "company": company.company_name,
        "email": company.hr_email,
        "drives": len(drives),
        "applications": applicants
    }), 200

#create drive
@company.route('/drive/create', methods=['POST'])
@role_required("company")
def create_drive():

    data = request.get_json()

    branches_name = data.get('branch')
    required_fields = ['title', 'description', 'branch', 'cgpa', 'year', 'deadline']

    for field in required_fields:
        if data.get(field) in [None, ""]:
            return jsonify ({"message": f"{field.capitalize()} is required"}), 400

    if not branches_name:
        return jsonify({"message": "Branch is required"}), 400
    
    if branches_name.lower() != "all":
        branch = Branch.query.filter_by(name=branches_name).first() if branches_name else None

        if not branch:
            return jsonify({"message": "Invalid branch name"}), 400
        
    else:
        branches_name = "All"

    user = db.session.get(User, session['user_id'])
    company = Company.query.filter_by(user_id=user.id).first()

    try: 
        cgpa = float(data.get('cgpa'))
        if cgpa < 0.0  or cgpa > 10.0:
            return jsonify({'message': "CGPA must be between 0.0 and 10.0"}), 400
    except ValueError:
        return jsonify({'message': "Invalid CGPA value"}), 400
    
    try: 
        year = int(data.get('year'))
        if year < 1 or year > 5:
            return jsonify({'message': "Year must be between 1 and 5 Means if 1st year write 1 if 2nd year write 2 accordingly"}), 400
    except ValueError:
        return jsonify({'message': "Invalid Year value;Means if 1st year write 1 if 2nd year write 2 accordingly"}), 400

    drive = Drive(
        company_id=company.id,
        title=data.get('title'),
        description=data.get('description'),
        branch=branches_name,
        cgpa = data.get('cgpa'),
        year = data.get('year'),
        deadline=data.get('deadline'),
        status='Pending'
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({'message': 'Drive created successfully'}), 201

@company.route("/update-profile", methods=["POST"])
@role_required("company")
def update_profile():

    user = db.session.get(User, session["user_id"])
    company = Company.query.filter_by(user_id=user.id).first()

    data = request.json

    company.company_name = data.get("company_name", company.company_name)
    company.website = data.get("website", company.website)
    company.hr_email = data.get("hr_email", company.hr_email)

    db.session.commit()

    return jsonify({
        "message": "Profile updated"
    })
#my drives
@company.route('/drives', methods=['GET']) 
@role_required("company") 
def my_drives():
    
    user = db.session.get(User, session['user_id'])
    company = Company.query.filter_by(user_id=user.id).first()
    drives = Drive.query.filter_by(company_id=company.id).all()

    data = []

    for d in drives:

        applicants = Application.query.filter_by(drive_id=d.id).count()
        data.append({
            "id": d.id,
        "title": d.title,
        "description": d.description,
        "branch": d.branch,
        "cgpa": d.cgpa,
        "year": d.year,
        "deadline": d.deadline,
        "status": d.status,
        "applicants": applicants})

    return jsonify(data), 200


#view applications for a drive
@company.route('/applications/<int:drive_id>', methods=['GET'])
@role_required("company")
def drive_applications(drive_id):

    user = db.session.get(User, session['user_id'])
    company = Company.query.filter_by(user_id=user.id).first()

    drive = Drive.query.get_or_404(drive_id)

    if drive.company_id != company.id:
        return jsonify({'message': 'Unauthorized access'}), 403

    applications = Application.query.filter_by(drive_id=drive.id).all()

    data = []

    for app in applications:
        student = db.session.get(Student,app.student_id)
        user = db.session.get(User,student.user_id)

        data.append({
            "application_id": app.id,
            "student": user.name,
            "email": user.email,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "year": student.year,
            "resume": (
    f"http://localhost:5000/uploads/{student.resume}"
    if student.resume
    else None
),
            "status": app.status,
            "application_date": app.applied_at,
            "interview_date": app.interview_date,
            "interview_link":app.interview_link
        })

    return jsonify(data), 200


#update application status
@company.route("/application/update/<int:id>", methods=["POST"])
@role_required("company")
def update_application(id):

    application = db.session.get(Application, id)

    if application is None:
        return jsonify({"message":"Application not found"}),404

    drive = db.session.get(Drive, application.drive_id)

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({"message":"Unauthorized"}),403

    data = request.json
    allowed_statuses = ["Pending","Applied", "Shortlisted", "Rejected","Selected","Interview Scheduled"]
    status = data.get("status")

    if status not in allowed_statuses:
        return jsonify({"message": "invalid status"}), 400
    
    application.status = status
    application.status_updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message":"Status Updated"})


#scheduling interview
@company.route("/application/schedule/<int:id>", methods=["POST"])
@role_required("company")
def shedule_interview(id):

    application = db.session.get(Application, id)

    if application is None:
        return jsonify({"message":"Application not found"}),404
    
    drive = db.session.get(Drive, application.drive_id)

    company_data = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company_data.id:
        return jsonify({"message": "Unauthorized access"}), 403
    
    data = request.get_json()

    if not data.get("interview_date") :
        return jsonify({"message": "Interview date is required"}), 400
    
    application.interview_date = data.get("interview_date")
    application.interview_link = ("https://meet.google.com/")
    application.status = "Interview Scheduled"
    application.status_updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"message":"Interview Scheduled","interview_link":application.interview_link}), 200


@company.route("/get-profile", methods=["GET"])
@role_required("company")
def get_profile():

    user = db.session.get(User, session["user_id"])
    company = Company.query.filter_by(user_id=user.id).first()

    return jsonify({
        "company_name": company.company_name,
        "website": company.website,
        "hr_email": company.hr_email,
        "email": user.email
    })



@company.route("/drive/<int:id>", methods=["PUT"])
@role_required("company")
def update_drive(id):

    drive = db.session.get(Drive, id)

    if drive is None:
        return jsonify({"message": "Drive not found"}), 404

    company = Company.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if drive.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    data = request.get_json()

    # Validate required fields
    required_fields = [
        "title",
        "description",
        "branch",
        "cgpa",
        "year",
        "deadline"
    ]

    for field in required_fields:
        if data.get(field) in [None, ""]:
            return jsonify({
                "message": f"{field.capitalize()} is required"
            }), 400

    # Update drive
    drive.title = data["title"]
    drive.description = data["description"]
    drive.branch = data["branch"]
    drive.cgpa = float(data["cgpa"])
    drive.year = int(data["year"])
    drive.deadline = data["deadline"]

    # Require admin approval again after editing
    drive.status = "Pending"

    db.session.commit()

    return jsonify({
        "message": "Drive updated successfully and sent for admin approval."
    }), 200