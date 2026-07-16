import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR,"instance")
SESSION_DIR = os.path.join(BASE_DIR,"flask_session")

os.makedirs(INSTANCE_DIR, exist_ok=True)
os.makedirs(SESSION_DIR, exist_ok=True)

class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            INSTANCE_DIR,
            "placement.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = SESSION_DIR
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False