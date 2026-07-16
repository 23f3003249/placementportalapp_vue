from flask import Blueprint, request, jsonify, session
from database import db 
from models import User, Student, Company, Drive, Application, Branch
from sqlalchemy import or_
from cache import delete_cache_pattern

from auth_utils import role_required

admin = Blueprint('admin', __name__)

#admindashboard 
@admin.route('/dashboard', methods=['GET'])
@role_required("admin")
def admin_dashboard():

    return jsonify({
        "students": Student.query.count(),
        "companies":Company.query.count(),
        "drives": Drive.query.count(),
        "applications": Application.query.count()
    }), 200

#students
@admin.route('/students', methods=['GET'])
@role_required("admin")
def students():

    data = []
    for s in Student.query.all():
        user= db.session.get(User,s.user_id)

        data.append({
            "id": s.id,
            "name": user.name,
            "email": user.email,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "year": s.year,
            "resume": s.resume,
            "active": user.active
        })

    return jsonify(data), 200
    

#for companies
@admin.route('/companies', methods=['GET'])
@role_required("admin")
def companies():

    data = []
    for c in Company.query.all():
        user = db.session.get(User,c.user_id)

        data.append({
            "id": c.id,
            "company_name": c.company_name,
            "email": c.hr_email,
            "approved": user.approved,
            "active": user.active
            })
        
    return jsonify(data), 200
    
#approving company
@admin.route('/approve-company/<int:id>', methods=['POST'])
@role_required("admin")
def approve_company(id):

    company = Company.query.get_or_404(id)

    if not company:
        return jsonify({'message': 'Company not found'}), 404
    
    user = db.session.get(User,company.user_id)
    user.approved = True

    db.session.commit()

    return jsonify({'message': 'Company approved successfully'}), 200

#reject company
@admin.route("/reject-company/<int:id>",methods=["POST"])
@role_required("admin")
def reject_company(id):

    company=Company.query.get_or_404(id)

    user=db.session.get(User,company.user_id)

    db.session.delete(company)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message":"Company Rejected"})


#drives
@admin.route('/drives', methods=['GET'])
@role_required("admin")
def drives():

    
    data = []

    for d in Drive.query.all():
        company = db.session.get(Company,d.company_id)

        data.append({
            "id": d.id,
            "title": d.title,
            "company": company.company_name,
            "description": d.description,
            "branch": d.branch,
            "deadline": d.deadline,
            "status": d.status,
            
        })

    return jsonify(data), 200
    
#approvving drives
@admin.route('/approve-drive/<int:id>', methods=['POST'])
@role_required("admin")
def approve_drive(id):

    drive = Drive.query.get_or_404(id)
    
    drive.status = "Approved"
    db.session.commit()

    delete_cache_pattern("approved_drives_*")

    return jsonify({'message': 'Drive approved successfully'}), 200


#rejecting drive 
@admin.route('/reject-drive/<int:id>', methods=['POST'])
@role_required("admin")
def reject_drive(id):

    drive = db.session.get(Drive, id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404
    
    drive.status = "Rejected"
    db.session.commit()

    delete_cache_pattern("approved_drives_*")

    return jsonify({"message": 'Drive Rejected'})


#blacklisting student
@admin.route('/blacklist-student/<int:id>', methods=['POST'])
@role_required("admin")
def blacklist_student(id):


    student = Student.query.get_or_404(id)
    user = db.session.get(User,student.user_id)
    user.active = False

    db.session.commit()
    return jsonify({'message':'Student Blacklisted'})



#blacklisting company  
@admin.route('/blacklist-company/<int:id>', methods=['POST'])
@role_required("admin")
def blacklist_company(id):

    company = Company.query.get_or_404(id)
    user = db.session.get(User,company.user_id)
    user.active = False

    db.session.commit()

    return jsonify({'message': 'Company blacklisted successfully'}), 200

#all applications
@admin.route('/applications', methods=['GET'])
@role_required("admin")
def applications():

    data = []

    for a in Application.query.all():
        student = db.session.get(Student,a.student_id)
        drive = db.session.get(Drive,a.drive_id)
        company = db.session.get(Company,drive.company_id)

        data.append({
            "student_name": User.query.get(student.user_id).name,
            "company_name": company.company_name,
            "drive_title": drive.title,
            "application_date": a.applied_at,
            "status": a.status
        })

    return jsonify(data), 200


#searching student
@admin.route('/search/students', methods=['GET'])
@role_required("admin")
def search_students():

    query = request.args.get('q', '')
    students = db.session.query(Student,User).join(User,Student.user_id==User.id).filter(or_( User.name.ilike(f"%{query}%"),
                                                                                        User.email.ilike(f"%{query}%"),
                                                                                        Student.branch.ilike(f"%{query}%"))).all()

    data = []
    for s,user in students:
        data.append({
            "id": s.id,
            "name": user.name,
            "email": user.email,
            "branch": s.branch,
            "cgpa": s.cgpa,
            "year": s.year,
            "resume": s.resume,
            "active": user.active
        })

    return jsonify(data), 200

#search companies
@admin.route('/search/companies', methods=['GET'])
@role_required("admin")
def search_companies():
 
    query = request.args.get('q', '')

    companies = db.session.query(Company,User).join(User,Company.user_id==User.id).filter(or_( Company.company_name.ilike(f"%{query}%"),
                                                                                        User.email.ilike(f"%{query}%"))).all()

    data = []
    for c,user in companies:
        data.append({
            "id": c.id,
            "company_name": c.company_name,
            "email": c.hr_email,
            "approved": user.approved,
            "active": user.active
        })

    return jsonify(data), 200


#search drives 
@admin.route('/search/drives', methods=['GET'])
@role_required("admin")
def search_drives():

    query = request.args.get('q', '')
    drives = db.session.query(Drive,Company).join(Company,Drive.company_id == Company.id).filter(or_( Drive.title.ilike(f"%{query}%"),
                                                                                        Company.company_name.ilike(f"%{query}%"))).all()

    data = []
    for d,company in drives:

        data.append({
            "id": d.id,
            "title": d.title,
            "company": company.company_name,
            "description": d.description,
            "branch": d.branch,
            "deadline": d.deadline,
            "status": d.status
        })

    return jsonify(data), 200


@admin.route('/statistics', methods=['GET'])
@role_required("admin")
def statistics():

    return jsonify({
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": Drive.query.count(),
        "total_applications": Application.query.count(),
        "selected_students" : Application.query.filter_by(status="Selected").count(),
        "rejected_students" : Application.query.filter_by(status="Rejected").count(),
        "shortlisted_students" : Application.query.filter_by(status="Shortlisted").count()
    }), 200


@admin.route('/branches', methods=['GET'])
@role_required("admin")
def get_branches():

    branch = Branch.query.order_by(Branch.name).all()
    return jsonify([
        {
            "id": branch.id,
            "name": branch.name
        }
        for branch in branch
    ])

@admin.route('/branches', methods=['POST'])
@role_required("admin")
def add_branch():
  
    data = request.get_json()
    name = data.get('name','').strip().upper()

    if not name:
        return jsonify({"message": "Branch name is required"}), 400
    
    existing_branch = Branch.query.filter(
        db.func.lower(Branch.name) == name.lower()
    ).first()

    if existing_branch:
        return jsonify({"message": "Branch already exists"}), 400
    
    branch = Branch(name=name)
    db.session.add(branch)
    db.session.commit()

    return jsonify({
        "message": "Branch added successfully"
    }), 201


@admin.route("/branches/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_branch(id):

  
    branch = db.session.get(Branch, id)

    if branch is None:
        return jsonify({"message": "Branch not found"}), 404

    # Don't delete if any student uses it
    student_exists = Student.query.filter_by(branch=branch.name).first()

    if student_exists:
        return jsonify({
            "message": "Branch is assigned to one or more students"
        }), 400

    # Don't delete if any drive uses it
    drive_exists = Drive.query.filter_by(branch=branch.name).first()

    if drive_exists:
        return jsonify({
            "message": "Branch is used by one or more drives"
        }), 400

    db.session.delete(branch)
    db.session.commit()

    return jsonify({
        "message": "Branch deleted successfully"
    }), 200


@admin.route(
    "/details/<string:item_type>/<int:item_id>",
    methods=["GET"]
)
@role_required("admin")
def get_details(item_type, item_id):

    if item_type == "company":

        company = db.session.get( Company,item_id)

        if company is None:
            return jsonify({
                "message": "Company not found"
            }), 404

        user = db.session.get(
            User,
            company.user_id
        )

        return jsonify({
            "type": "company",
            "title": company.company_name,
            "details": {
                "Company ID": company.id,
                "Company Name": company.company_name,
                "Login Email": user.email,
                "HR Email": company.hr_email,
                "Website": company.website or "Not provided",
                "Approval Status": (
                    "Approved"
                    if user.approved
                    else "Pending"
                ),
                "Account Status": (
                    "Active"
                    if user.active
                    else "Blocked"
                )
            }
        }), 200


    if item_type == "student":

        student = db.session.get(Student,item_id)

        if student is None:
            return jsonify({
                "message": "Student not found"
            }), 404

        user = db.session.get(User,student.user_id)

        application_count = (
            Application.query.filter_by(
                student_id=student.id
            ).count()
        )

        return jsonify({
            "type": "student",
            "title": user.name,
            "details": {
                "Student ID": student.id,
                "Name": user.name,
                "Email": user.email,
                "Branch": student.branch,
                "CGPA": student.cgpa,
                "Year": student.year,
                "Resume": (
                    student.resume
                    or "Not uploaded"
                ),
                "Applications": application_count,
                "Account Status": (
                    "Active"
                    if user.active
                    else "Blocked"
                )
            }
        }), 200


    if item_type == "drive":

        drive = db.session.get(Drive,item_id)

        if drive is None:
            return jsonify({
                "message": "Drive not found"}), 404

        company = db.session.get(
            Company,
            drive.company_id
        )

        applicant_count = (
            Application.query.filter_by(
                drive_id=drive.id
            ).count()
        )

        return jsonify({
            "type": "drive",
            "title": drive.title,
            "details": {
                "Drive ID": drive.id,
                "Company": company.company_name,
                "Job Title": drive.title,
                "Description": drive.description,
                "Eligible Branch": drive.branch,
                "Minimum CGPA": drive.cgpa,
                "Eligible Year": drive.year,
                "Deadline": drive.deadline,
                "Status": drive.status,
                "Applicants": applicant_count
            }
        }), 200


    if item_type == "application":

        application = db.session.get(Application,item_id)

        if application is None:
            return jsonify({
                "message": "Application not found"
            }), 404

        student = db.session.get(Student,application.student_id)
        student_user = db.session.get( User,student.user_id)

        drive = db.session.get(Drive,application.drive_id)
        company = db.session.get(Company,drive.company_id)

        return jsonify({
            "type": "application",
            "title": "Application Details",
            "details": {
                "Application ID": application.id,
                "Student": student_user.name,
                "Company": company.company_name,
                "Drive": drive.title,
                "Status": application.status,
                "Applied At": (
                    application.applied_at.strftime(
                        "%d-%m-%Y %H:%M"
                    )
                ),
                "Interview Date": (
                    application.interview_date
                    or "Not scheduled"
                ),
                "Interview Link": (
                    application.interview_link
                    or "Not available"
                )
            }
        }), 200

    return jsonify({
        "message": "Invalid details type"
    }), 400