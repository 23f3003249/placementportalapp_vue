from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv


load_dotenv()

from config import Config
from database import db
from models import User


def create_app():

    #flask app intialization
    app = Flask(__name__)
    app.config.from_object(Config)

    #cors intialization
    CORS(app,origins=["http://localhost:5173"],supports_credentials=True)

    #intializing flask session
    Session(app)
    db.init_app(app)



    # Upload folder
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER,exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # Resume / uploaded file route
    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"],filename)

    # Register Blueprints
    from routes.auth import auth
    from routes.admin import admin
    from routes.student import student
    from routes.company import company

    app.register_blueprint(auth,url_prefix="/auth")
    app.register_blueprint(admin,url_prefix="/admin")
    app.register_blueprint(student,url_prefix="/student" )
    app.register_blueprint(company,url_prefix="/company")

    # Database
    with app.app_context():

        db.create_all()

        admin = User.query.filter_by(email=os.getenv("ADMIN_EMAIL")).first()

        if admin is None:

            admin = User(
                name="Admin",
                email=os.getenv("ADMIN_EMAIL"),
                password=generate_password_hash(
                    password=os.getenv(
                        "ADMIN_PASSWORD"
                    )
                ),
                role="admin",
                approved=True,
                active=True
            )

            db.session.add(admin)
            db.session.commit()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)