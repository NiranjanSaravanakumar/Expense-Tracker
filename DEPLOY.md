# 🚀 Deploying Expense Tracker — Vercel + Supabase

> **Why Supabase over Firebase?**
> Your app uses SQLAlchemy with relational data (users → expenses via foreign keys).
> Supabase is PostgreSQL — your models work with **zero schema changes**.
> Firebase (Firestore) is NoSQL and would require rewriting all models and queries.

---

## 📋 Overview

```
Local (Dev)          →   Production
──────────────────────────────────────
Flask (run.py)       →   Vercel (Serverless Python)
SQLite (.db file)    →   Supabase (PostgreSQL)
.env (local)         →   Vercel Environment Variables
```

---

## PART 1 — Set Up Supabase (Database)

### Step 1: Create a Supabase account and project
1. Go to https://supabase.com → click **Start for Free**
2. Sign in with GitHub
3. Click **New Project** and fill in:
   - **Name**: `expense-tracker`
   - **Database Password**: choose a strong password *(save it!)*
   - **Region**: `ap-southeast-1` (Singapore — closest to India)
4. Wait ~2 minutes for the project to be provisioned

### Step 2: Get your PostgreSQL connection string
1. Supabase Dashboard → **Project Settings** → **Database**
2. Scroll to **Connection String** → select the **URI** tab
3. Copy the string — it looks like:
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxx.supabase.co:5432/postgres
   ```
4. Replace `[YOUR-PASSWORD]` with your actual password and **save this string** — you'll need it in Step 10

---

## PART 2 — Update the Flask Project

### Step 3: Activate your virtual environment
```powershell
venv\Scripts\activate
```

### Step 4: Install the PostgreSQL driver
```powershell
pip install psycopg2-binary
```

### Step 5: Update `requirements.txt`
Add `psycopg2-binary` to the file:
```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.2
python-dotenv==1.0.1
Werkzeug==3.1.3
email-validator==2.2.0
WTForms==3.2.1
psycopg2-binary==2.9.9
```

### Step 6: Update `config.py`
Make sure it reads `DATABASE_URL` from environment (so it uses SQLite locally and PostgreSQL on Vercel):
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # Uses DATABASE_URL (Supabase) in production, falls back to SQLite locally
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///expense_tracker.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Step 7: Create `api/index.py` (Vercel entry point)
Create a new folder `api/` in the project root, then create `api/index.py`:
```python
# api/index.py — Vercel serverless entry point for Flask
from app import create_app

app = create_app()
```

Your project structure should look like:
```
Expense-Tracker/
├── api/
│   └── index.py        ← NEW
├── app/
├── venv/
├── config.py
├── run.py
├── requirements.txt
└── vercel.json         ← NEW (next step)
```

### Step 8: Create `vercel.json` in the project root
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### Step 9: Update `.gitignore`
Ensure sensitive/unnecessary files are excluded from Git:
```
venv/
__pycache__/
*.pyc
instance/
.env
*.db
```

---

## PART 3 — Push to GitHub

### Step 10: Initialize Git and push your project
```powershell
# Initialize git repo (if not done already)
git init

# Stage all files
git add .

# Commit
git commit -m "feat: prepare for Vercel + Supabase deployment"
```

1. Go to https://github.com/new and create a **new empty repository** (do NOT add README)
2. Copy the remote URL and run:
```powershell
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker.git
git push -u origin main
```

---

## PART 4 — Deploy on Vercel

### Step 11: Import your project on Vercel
1. Go to https://vercel.com → sign in with GitHub
2. Click **Add New Project**
3. Find and **Import** your `expense-tracker` repository
4. On the Configure screen:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./` (default)

### Step 12: Set Environment Variables
Before clicking Deploy, click **Environment Variables** and add these 3 variables:

| Variable Name  | Value                                                                 |
|----------------|-----------------------------------------------------------------------|
| `SECRET_KEY`   | Any long random string e.g. `expense-tracker-secret-2026!`           |
| `DATABASE_URL` | `postgresql+psycopg2://postgres:[PASSWORD]@db.xxxx.supabase.co:5432/postgres` |
| `FLASK_ENV`    | `production`                                                          |

> ⚠️ IMPORTANT: If your Supabase URL starts with `postgres://`, change it to `postgresql+psycopg2://`

### Step 13: Deploy!
Click **Deploy** and wait ~1 minute.

### Step 14: Initialize the database
Visit your live URL (e.g. `https://expense-tracker-abc.vercel.app`).

Since `create_app()` already calls `db.create_all()`, all your tables are **automatically created on the first request** — no manual migration needed!

---

## ✅ Go-Live Checklist

- [ ] Supabase project is running and connection string is copied
- [ ] `psycopg2-binary` added to `requirements.txt`
- [ ] `config.py` reads `DATABASE_URL` from environment
- [ ] `api/index.py` created
- [ ] `vercel.json` created in project root
- [ ] Code pushed to GitHub
- [ ] Vercel project imported and environment variables set:
  - [ ] `SECRET_KEY`
  - [ ] `DATABASE_URL` (using `postgresql+psycopg2://` prefix)
  - [ ] `FLASK_ENV=production`
- [ ] First visit to live URL triggers DB table creation
- [ ] Can register and log in on the live site

---

## ⚠️ Common Issues & Fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| `could not connect to server` | Wrong `DATABASE_URL` | Double-check the URL and password in Vercel env vars |
| `Module 'psycopg2' not found` | Missing driver | Add `psycopg2-binary==2.9.9` to `requirements.txt` |
| CSRF / `400 Bad Request` on forms | Missing `SECRET_KEY` | Set `SECRET_KEY` in Vercel environment variables |
| `postgres://` driver error | Wrong URL prefix | Change `postgres://` → `postgresql+psycopg2://` |
| Static files (CSS/JS) not loading | Static folder not found | Ensure `app/static/` exists and Flask's static handler is active |
| Blank page / 500 error | Runtime crash | Check Vercel **Function Logs** in the dashboard for error details |

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Supabase Dashboard | https://supabase.com/dashboard |
| Vercel Dashboard | https://vercel.com/dashboard |
| Vercel Python Docs | https://vercel.com/docs/functions/runtimes/python |
| Supabase Connection Docs | https://supabase.com/docs/guides/database/connecting-to-postgres |


 Your Project Structure is Now Ready
Expense-Tracker/
├── api/
│   └── index.py        ← Vercel entry point
├── app/
├── vercel.json         ← Vercel config
├── requirements.txt    ← Includes psycopg2-binary
├── config.py           ← Reads DATABASE_URL from env
└── .gitignore          ← Excludes .env and *.db
▶️ Next Steps (from 

DEPLOY.md
)
Create Supabase project → get your DATABASE_URL string
Push to GitHub → git init → git push
Import on Vercel → set SECRET_KEY + DATABASE_URL env vars → Deploy!
