# Placement Portal App (Vue)

A web-based Placement Management System designed for **Admins, Companies, and Students** to manage placement activities efficiently.

## Tech Stack

- **Frontend:** Vue.js, Bootstrap 5
- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy
- **Task Queue:** Celery
- **Message Broker:** Redis
- **Email Service:** Mailtrap

---

## Run the Application

Follow the steps below to start the application. Each service should be started in a **separate terminal** from the project root directory.

### 1. Start Redis

Make sure Docker is running, then execute:

```bash
docker start redis
```

### 2. Start the Flask Backend

Open a terminal and run:

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

The backend will be available at:

**http://localhost:5000**

### 3. Start the Celery Worker

Open a **new terminal** and run:

```bash
cd backend

celery -A celery_app.celery worker --loglevel=info --pool=solo
```

This starts the Celery worker to process background tasks.

### 4. Start Celery Beat

Open **another terminal** and run:

```bash
cd backend

celery -A celery_app.celery beat --loglevel=info
```

This starts Celery Beat to schedule periodic background tasks.

### 5. Start the Vue Frontend

Open a **new terminal** and run:

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at:

**http://localhost:5173**

---

## Environment Variables

Create a `.env` file inside the `backend` directory.

Add the following environment variables and replace the placeholder values with your actual credentials:

```env
ADMIN_EMAIL=your_admin_email
ADMIN_PASSWORD=your_admin_password

MAILTRAP_USERNAME=your_mailtrap_username
MAILTRAP_PASSWORD=your_mailtrap_password
```

**Note:** Keep your `.env` file private. Do not commit actual credentials or passwords to GitHub.

---

## Application URLs

| Service | URL |
| Vue Frontend | http://localhost:5173 |
| Flask Backend | http://localhost:5000 |

---
## Project Name

**placementportalapp_vue**
