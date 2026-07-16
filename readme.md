A web-based placement management system for Admin, Companies, and Students.

Run the Application

## Start Redis

docker start redis

## Start Flask Backend

cd backend
pip install -r requirements.txt
python app.py

Backend runs on http://localhost:5000.

## Start Celery Worker

### Open a new terminal:

cd backend
celery -A celery_app.celery worker --loglevel=info --pool=solo 4. Start Celery Beat

### Open another terminal:

cd backend
celery -A celery_app.celery beat --loglevel=info 5. Start Vue Frontend

### Open another terminal:

cd frontend
npm install
npm run dev

Frontend runs on http://localhost:5173.

Environment Variables

Create a .env file inside the backend folder and configure:

ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password
MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password
Tech Stack

Flask, Vue.js, Bootstrap 5, SQLite, Redis, Celery, SQLAlchemy, and Mailtrap.
# placementportalapp_vue
# placementportalapp_vue
