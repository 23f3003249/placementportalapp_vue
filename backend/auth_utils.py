from functools import wraps

from flask import jsonify, session

from database import db
from models import User

def get_current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    user = db.session.get(User, user_id)
    if user is None:
        session.clear()
        return None
    return user


def role_required(required_role):
    def decorator(view_function):
        @wraps(view_function)
        def wrapped_view(*args, **kwargs):
            user = get_current_user()

            if user is None:
                return jsonify({"message": "Authentication required"}), 401

            if not user.active:
                session.clear()
                return jsonify({"message": "Account deactivated"}), 403

            if user.role != required_role:
                return jsonify({"message": "Access forbidden"}), 403

            if (required_role == "company" and not user.approved):
                return jsonify({"message": "Company approval required"}), 403

            return view_function(*args, **kwargs)
        return wrapped_view
    return decorator