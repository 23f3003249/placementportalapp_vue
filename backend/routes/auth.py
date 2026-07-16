from flask import request, jsonify, Blueprint,session
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models import User, Student, Company, Branch

auth = Blueprint('auth', __name__)


@auth.route('/register/student', methods=['POST'])
def register_student():
    try:
        data = request.get_json()

        branches_name = data.get('branch')
        if not branches_name:
            return jsonify({"message": "Branch is required"}), 400

        branch = Branch.query.filter(db.func.lower(Branch.name) == branches_name.lower()).first()

        if not branch: 
            return jsonify({"message": "Invalid branch name"}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
    
        user = User(
            name = data['name'],
            email = data['email'],
            password = generate_password_hash(data['password']),
            role = 'student',
            approved = True,
            active = True
        )

        db.session.add(user)
        db.session.flush()
    
        student = Student(
            user_id = user.id,
            branch = data.get("branch"),
            cgpa = data.get('cgpa',0.0),
            year = data.get('year',1),
            resume = ""
        )

        db.session.add(student)
        db.session.commit()
        return jsonify({'message': 'Student registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred during registration', 'error': str(e)})
    

@auth.route('/register/company', methods=['POST'])
def register_company():
    try:
        data = request.get_json()

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
    
        if Company.query.filter_by(
                company_name=data['company_name']
            ).first():
                return jsonify({'message': 'Company name not available'}), 400
        
        user = User(
            name = data.get('company_name'),
            email = data['email'],
            password = generate_password_hash(data['password']),
            role = 'company',
            approved = False,
            active = True
        )

        db.session.add(user)
        db.session.flush()
        
        company = Company(
            user_id = user.id,
            company_name = data.get('company_name'),
            website = data.get("website"),
            hr_email=data.get("hr_email")
        )

        db.session.add(company)
        db.session.commit()

        return jsonify({'message': 'Company registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error occurred during registration', 'error': str(e)}), 500


#login
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No input data provided"}), 400

    if not data.get("email"):
        return jsonify({"message": "Email is required"}), 400
    
    if not data.get("password"):
        return jsonify({"message": "Password is required"}), 400

    user = User.query.filter_by(email=data["email"].strip()).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user.password,data["password"]):
        return jsonify({"message": "Wrong password"}), 401
    
    if user.role == "company" and not user.approved:
        return jsonify({"message": "Company not approved"}), 403
    
    if not user.active:
        return jsonify({"message": "Your account has been blocked bby the admin"}), 403
    
    
    session.clear()
    session["user_id"] = user.id
    session["user_role"] = user.role

    session.modified = True

    return jsonify({

        "message": "Login Successful",
        "role": user.role
    }), 200



@auth.route('/logout', methods=['POST'])
def logout():
    
    session.clear()
    return jsonify({
        "message": "Logged Out"
    }),200



@auth.route('/current-user', methods=['GET'])
def me():
    if "user_id" not in session:
        return jsonify({"message": "Login required"}), 401
    
    current_user = db.session.get(User, session["user_id"])
    
    if current_user is None:
        session.clear()
        return jsonify({"message": "User not found"}), 404

    if not current_user.active:
        session.clear()
        return jsonify({"message": "Your account has been blocked by admin"}), 403
    
    if current_user.role == "company" and not current_user.approved:
        return jsonify({"message": "Company not approved"}), 403
    
    return jsonify({
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "approved": current_user.approved,
        "active" : current_user.active
    }),200


@auth.route('/branches', methods=['GET'])
def get_branches():
    
    branches = Branch.query.order_by(Branch.name).all()
    return jsonify([
        {
            "id": branch.id,
            "name": branch.name
        }
        for branch in branches
    ])

