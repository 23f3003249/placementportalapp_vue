from flask import Blueprint, request, jsonify, session, current_app as app, send_file
from database import db
from datetime import datetime
from models import User, Student, Company, Drive, Application,Branch
from sqlalchemy import or_

from auth_utils import role_required

from cache import get_cache, set_cache, delete_cache
from werkzeug.utils import secure_filename


import os
import csv

student = Blueprint('student', __name__)


#student dashboard
@student.route('/dashboard', methods=['GET'])
@role_required("student")
def student_dashboard():

    
    student_user = db.session.get(User,session['user_id'])
    student = Student.query.filter_by(user_id=student_user.id).first()

    applied = Application.query.filter_by(student_id=student.id).count()

    return jsonify({
        "name": student_user.name,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "applied": applied
    }), 200

#approved details 
@student.route("/drives")
@role_required("student")
def drives():

    student_user = db.session.get(
        User,
        session["user_id"]
    )

    student = Student.query.filter_by(
        user_id=student_user.id
    ).first()

    if student is None:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    cache_key = f"approved_drives_{student.id}"

    cached_drives = get_cache(cache_key)

    if cached_drives is not None:
        return jsonify(cached_drives), 200

    data = []

    approved_drives = Drive.query.filter_by(
        status="Approved"
    ).all()

    for d in approved_drives:

        if student.cgpa < d.cgpa:
            continue

        if student.year != d.year:
            continue

        if (
            d.branch.lower() != "all"
            and student.branch.lower()
            != d.branch.lower()
        ):
            continue

        try:
            deadline = datetime.strptime(
                d.deadline,
                "%Y-%m-%d"
            ).date()

        except ValueError:
            continue

        if deadline < datetime.now().date():
            continue

        company = db.session.get(
            Company,
            d.company_id
        )

        if company is None:
            continue

        data.append({
            "id": d.id,
            "company": company.company_name,
            "title": d.title,
            "branch": d.branch,
            "cgpa": d.cgpa,
            "deadline": d.deadline
        })

    set_cache(
        cache_key,
        data,
        expiry=3500
    )

    return jsonify(data), 200

@student.route(
    "/drive/<int:drive_id>",
    methods=["GET"]
)
@role_required("student")
def drive_details(drive_id):

    student_user = db.session.get(
        User,
        session["user_id"]
    )

    student_profile = (
        Student.query.filter_by(
            user_id=student_user.id
        ).first()
    )

    if student_profile is None:

        return jsonify({
            "message":
            "Student profile not found"
        }), 404


    drive = db.session.get(
        Drive,
        drive_id
    )


    if drive is None:

        return jsonify({
            "message": "Drive not found"
        }), 404


    if drive.status != "Approved":

        return jsonify({
            "message":
            "Drive is not available"
        }), 403


    if student_profile.cgpa < drive.cgpa:

        return jsonify({
            "message":
            "You are not eligible for this drive"
        }), 403


    if student_profile.year != drive.year:

        return jsonify({
            "message":
            "You are not eligible for this drive"
        }), 403


    if (
        drive.branch.lower() != "all"
        and
        student_profile.branch.lower()
        != drive.branch.lower()
    ):

        return jsonify({
            "message":
            "You are not eligible for this drive"
        }), 403


    try:

        deadline = datetime.strptime(
            drive.deadline,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return jsonify({
            "message":
            "Invalid drive deadline"
        }), 500


    if deadline < datetime.now().date():

        return jsonify({
            "message":
            "Application deadline has passed"
        }), 403


    company = db.session.get(
        Company,
        drive.company_id
    )


    return jsonify({

        "id": drive.id,

        "company":
            company.company_name,

        "title":
            drive.title,

        "description":
            drive.description,

        "branch":
            drive.branch,

        "cgpa":
            drive.cgpa,

        "year":
            drive.year,

        "deadline":
            drive.deadline,

        "status":
            drive.status,

    }), 200

#application history
@student.route("/history")
@role_required("student")
def history():

    # if not is_student():
    #     return jsonify({"message": "Login required"}), 401

    student_user = db.session.get(User,session['user_id'])
    student = Student.query.filter_by(user_id=student_user.id).first()

    data = []

    applications = Application.query.filter_by(student_id=student.id).all()

    for a in applications:

        drive = db.session.get(Drive,a.drive_id)
        company = db.session.get(Company,drive.company_id)

        data.append({
            "company": company.company_name,
            "title": drive.title,
            "status": a.status,
            "date": a.applied_at.strftime("%d-%m-%Y"),
            "interview_date": a.interview_date,
            "interview_link": a.interview_link
        })

    return jsonify(data)


@student.route("/get-profile", methods=['GET'])
@role_required("student")
def get_profile():

    # if not is_student():
    #     return jsonify({"message": "Unathorized access"}), 403
    

    user = db.session.get(User,session['user_id'])
    student = Student.query.filter_by(user_id=session["user_id"]).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404
    
    if student is None:
        return jsonify({"message":"Student profile not found"}), 404


    return jsonify({
        "name" : user.name,
        "email" :user.email,
        "branch" : student.branch,
        "cgpa": student.cgpa,
        "year": student.year,
        "resume":student.resume
    }), 200


#update profile
@student.route("/update-profile", methods=["POST"])
@role_required("student")
def update_profile():

    # if not is_student():
    #     return jsonify({"message": "Login required"}), 401

    data = request.get_json()

    branch_name = data.get("branch")
    branch = Branch.query.filter( db.func.lower(Branch.name) == branch_name.lower()).first() if branch_name else None

    if not branch:
        return jsonify({"message": "Invalid branch selected"}), 400
    student_user = db.session.get(User,session['user_id'])
    student = Student.query.filter_by(user_id=student_user.id).first()

    if student is None:
        return jsonify({"message": "Student profile not found"}), 404

    try:
        cgpa = float(data.get("cgpa"))

        if cgpa < 0 or cgpa > 10:
            return jsonify({
            "message": "CGPA must be between 0 and 10"
        }), 400

    except (TypeError, ValueError):
        return jsonify({
        "message": "Invalid CGPA value"}), 400


    try:
        year = int(data.get("year"))

        if year < 1 or year > 5:
            return jsonify({
            "message": "Year must be between 1 and 5"
        }), 400

    except (TypeError, ValueError):
        return jsonify({
        "message": "Invalid year value"
        }), 400


    student_user.name = data.get("name",student_user.name)
    student.branch = branch.name
    student.cgpa = cgpa
    student.year = year

    db.session.commit()

    delete_cache(f"approved_drives_{student.id}")

    return jsonify({
        "message": "Profile Updated"
    }), 200





@student.route("/upload-resume", methods=["POST"])
@role_required("student")
def upload_resume():
    # if not is_student():
    #     return jsonify({"message": "Unauthorized access"}), 403
    
    if 'resume' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['resume']

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    
    if not file.filename.lower().endswith(('.pdf')):
        return jsonify({"message": "Only PDF files are allowed"}), 400
    
    
    filename = secure_filename(f"{session['user_id']}_{file.filename}")

    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    file.save(path)

    student = Student.query.filter_by(user_id=session['user_id']).first()

    if student.resume:
        old_path = os.path.join(app.config['UPLOAD_FOLDER'],student.resume)

        if os.path.exists(old_path):
            os.remove(old_path)

    student.resume = filename
    db.session.commit()

    return jsonify({"message": "Resume uploaded successfully"}), 200


@student.route("/export",methods=["GET"])
@role_required("student")
def export_history():

    # if not is_student():
    #     return jsonify({"message": "Unauthorized accesss"}), 403
    
    from tasks.export import export_applications as export_task
    student = Student.query.filter_by(user_id=session["user_id"]).first()

    export_task.delay(student.id)

    return jsonify({"message":"Export is underprocess, you will receive the email after completion"}), 200



#search drives
@student.route("/search",methods=["GET"])
@role_required("student")
def search_drives():

    query = request.args.get("q","")

    drives = db.session.query(Drive,Company).join(Company, Drive.company_id == Company.id).filter(
        Drive.status == "Approved",
        or_(Drive.title.ilike(f"%{query}%"), Company.company_name.ilike(f"%{query}%"))
    ).all()

    student_data = Student.query.filter_by(user_id=session["user_id"]).first()

    data = []

    for d, company in drives:

        if student_data.cgpa < d.cgpa:
            continue
        if student_data.year != d.year:
            continue

        if (d.branch.lower() != "all" and student_data.branch.lower()!= d.branch.lower()):
            continue

        try:
            deadline = datetime.strptime(d.deadline,"%Y-%m-%d").date()
        except ValueError:
            continue

        if deadline < datetime.now().date():
            continue

        data.append({
            "id": d.id,
            "company": company.company_name,
            "title": d.title,
            "branch": d.branch,
            "cgpa": d.cgpa,
            "deadline": d.deadline
        })
    
    return jsonify(data)


@student.route("/apply/<int:drive_id>",methods=["POST"])
@role_required("student")
def apply_drive(drive_id):

    student_profile = Student.query.filter_by( user_id=session["user_id"]
    ).first()

    if student_profile is None:
        return jsonify({
            "message": "Student profile not found"
        }), 404

    drive = db.session.get(Drive,drive_id)

    if drive is None:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status != "Approved":
        return jsonify({"message": "Drive is not available"}), 400

    try:
        deadline = datetime.strptime(drive.deadline,"%Y-%m-%d").date()

    except ValueError:
        return jsonify({"message": "Invalid drive deadline"}), 400

    if deadline < datetime.now().date():
        return jsonify({"message": "Application deadline has passed"}), 400

    if student_profile.cgpa < drive.cgpa:
        return jsonify({"message": "CGPA criteria not met"}), 400

    if student_profile.year != drive.year:
        return jsonify({"message": "Year criteria not met"
        }), 400 

    if ( drive.branch.lower() != "all" and student_profile.branch.lower()!= drive.branch.lower()):
        return jsonify({"message": "Branch criteria not met"}), 400

    existing_application = (Application.query.filter_by(
            student_id=student_profile.id,
            drive_id=drive.id
        ).first()
    )

    if existing_application is not None:
        return jsonify({"message":"You have already applied for this drive"})

    application = Application(student_id=student_profile.id,
        drive_id=drive.id,
        status="Applied")

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully"
    }), 201