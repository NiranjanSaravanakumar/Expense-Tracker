# Expense Tracker Web Application

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

A professional, full-stack, responsive web application for tracking personal finances. Built utilizing Python, Flask, SQLite, SQLAlchemy, Bootstrap 5, and Chart.js.

## ✨ Features

- **Authentication System:** Secure registration & login workflow using `Werkzeug` password hashing and `Flask-Login`.
- **Expense Management (CRUD):** Add, update, view, and delete detailed expense entries.
- **Categorization & Filtering:** Filter multi-conditional expenses by Category, Month, and Year.
- **Interactive Dashboard:** Beautiful dark-mode UI with a JSON-fed Chart.js dynamic doughnut graph.
- **Monthly Insights & Reports:** Aggregate data reports providing progress bars and category groupings.
- **Enterprise-ready Architecture:** MVC pattern separating models, route blueprints, and service layers.

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.8+ installed on your system.

### 2. Setup environment and install dependencies
```bash
# Clone the repository (or extract files)
cd Tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### 3. Database & App Configuration
The `.env` file is already preset for local development using an SQLite database (`instance/expense_tracker.db`), but ensure the file exists within the root directly.
No explicit DB initialization script is required—SQLAlchemy will automatically configure `create_all()` tables upon initial run.

### 4. Run the application
```bash
python run.py
```

Open a web browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🏗️ Architecture Stack

- **Backend:** Flask / Python
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend Architecture:** Jinja2 Templating
- **Styling:** Bootstrap 5.3 + Custom Premium Dark UI (`style.css`)
- **Visuals:** Chart.js 4.4 via RESTful API Endpoint
- **Form Validation:** Flask-WTF / WTForms
- **Security:** CSRF Protection, Password Hashing

## 📦 Deployment Suggestions

For turning this into a live production application, we recommend deploying on **Render, Heroku, or PythonAnywhere**:

1. **Database update:** Switch SQLite to PostgreSQL by replacing the `DATABASE_URL` environment variable.
2. **Server config:** Add `gunicorn==21.2.0` to `requirements.txt`. Add a `Procfile` file containing `web: gunicorn run:app`.
3. **Security:** Update the `.env` placeholder `SECRET_KEY` variable using a cryptographic string, and set `FLASK_ENV=production`.
4. Deploy using standard Git hook mechanisms provided by hosting servers.

---
### Resume / Portfolio Snippet
**Full-Stack Python Developer | Personal Finance Web Application**
> Formulated a MVC Flask application managing user expense aggregates natively executing RESTful APIs for asynchronous UI updates utilizing Bootstrap 5 and dynamic Chart.js graphing. Enhanced secure access through Werkzeug encryption and centralized data operations via SQLAlchemy.
