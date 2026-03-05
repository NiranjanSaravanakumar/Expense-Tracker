# 🚀 HOW TO RUN — Expense Tracker

A step-by-step guide to **start** and **stop** the Expense Tracker application on Windows.

---

## ⚙️ One-Time Setup (First Run Only)

> Skip this section if you have already done the setup before.

### 1. Navigate to the project folder
Open **PowerShell** or **Command Prompt** and run:
```powershell
cd C:\Users\INNISAR4\PRO\Expense-Tracker
```

### 2. Create a virtual environment
```powershell
python -m venv venv
```

### 3. Activate the virtual environment
```powershell
venv\Scripts\activate
```
You should see `(venv)` appear at the start of your terminal prompt.

### 4. Install required packages
```powershell
pip install -r requirements.txt
```

---

## ▶️ Start the Application (Every Time)

> Run these steps each time you want to start the app.

### 1. Open PowerShell and navigate to the project folder
```powershell
cd C:\Users\INNISAR4\PRO\Expense-Tracker
```

### 2. Activate the virtual environment
```powershell
venv\Scripts\activate
```

### 3. Start the Flask server
```powershell
python run.py
```

### 4. Open the app in your browser
Once you see output like:
```
 * Running on http://127.0.0.1:5000
```
Open your browser and go to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## ⏹️ Stop the Application

### 1. Stop the server
In the terminal where `python run.py` is running, press:
```
Ctrl + C
```
You will see:
```
Keyboard interrupt received, exiting.
```

### 2. Deactivate the virtual environment (optional but clean)
```powershell
deactivate
```
The `(venv)` prefix will disappear from your prompt.

---

## ⚠️ Common Issues & Fixes

| Problem | Cause | Fix |
|---|---|---|
| `Fatal error in launcher` when running `pip` | venv was moved/renamed from its original location | Delete `venv\` folder and recreate it with `python -m venv venv` |
| `ModuleNotFoundError` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Another process is using the port | Run `netstat -ano \| findstr :5000` to find and kill the process, or change the port in `run.py` |
| `(venv)` not showing in prompt | Virtual environment not activated | Run `venv\Scripts\activate` again |

---

## 📋 Quick Reference

```
Start:   cd C:\Users\INNISAR4\PRO\Expense-Tracker  →  venv\Scripts\activate  →  python run.py
Stop:    Ctrl + C  →  deactivate
URL:     http://127.0.0.1:5000
```
