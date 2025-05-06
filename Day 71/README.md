# 🚀 Day 71: Deploying a Website (Flask)

## 🧽 Overview

A practical guide to deploying a **Flask** website using GitHub, Heroku, Gunicorn, SQLite, and PostgreSQL.

---

## 🪰 Topics Covered

- Preparing a Flask project for deployment
- Using GitHub as source control and deployment source
- Heroku setup and deployment
- Web server configuration with Gunicorn
- Managing databases: SQLite (local) and PostgreSQL (production)

---

## 🛠️ Project Preparation

### Basic Checklist (Flask-specific):

- [x] Flask app runs locally via `python app.py` or similar
- [x] `requirements.txt` includes all dependencies (`pip freeze > requirements.txt`)
- [x] `Procfile` created with `web: gunicorn app:app`
- [x] `.gitignore` includes `.env`, `__pycache__/`, etc.
- [x] Use `python-dotenv` to manage environment variables
- [x] App reads from `os.environ` in production

---

## 🌐 Version Control with GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repo-url>
git push -u origin main
```

- GitHub acts as both version control and Heroku deployment source.

---

## 🚧 Deploying to Heroku

### Setup

```bash
heroku login
heroku create <app-name>
```

### Deploy from GitHub

- Connect your GitHub repo via the Heroku dashboard under **Deploy** tab
- Enable automatic deploys (optional)
- Trigger manual deployment if needed

### Alternative: Deploy via CLI

```bash
git push heroku main
```

---

## 🔧 Using Gunicorn

Gunicorn is a production WSGI HTTP server for running Python web apps.

### Installation:

```bash
pip install gunicorn
```

### Add to `requirements.txt`

```bash
echo "gunicorn" >> requirements.txt
```

### Example `Procfile`:

```
web: gunicorn app:app  # For Flask
```

---

## 📁 Managing Databases

### Development: SQLite

- Lightweight and local; no additional setup required.
- Common default for development.

### Production: PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

- Heroku sets a `DATABASE_URL` env variable
- In your Flask app, use `os.environ.get("DATABASE_URL")` for production
- Optionally, use `sqlalchemy` or another ORM to abstract DB usage

---

## 🎓 Environment Configuration

### Store secrets locally in `.env` file:

```
SECRET_KEY=your-secret
DEBUG=False
DATABASE_URL=sqlite:///local.db
```

### Access with `python-dotenv`:

```bash
pip install python-dotenv
```

In your Flask app (e.g., `app.py`):

```python
from dotenv import load_dotenv
load_dotenv()
```

Use environment variables via:

```python
import os
os.environ.get("SECRET_KEY")
```

---

## ✅ Quick Reference Checklist

- [x] Flask app structure is functional
- [x] All dependencies listed in `requirements.txt`
- [x] `.env` is excluded via `.gitignore`
- [x] `Procfile` is correctly defined for Gunicorn
- [x] GitHub repo is linked and pushed
- [x] Heroku app created and PostgreSQL added
- [x] Environment variables accessed via `os.environ`

---

## 📚 Further Reading

- [Heroku Docs](https://devcenter.heroku.com/)
- [Gunicorn Docs](https://docs.gunicorn.org/en/stable/)
- [Python-PostgreSQL](https://www.psycopg.org/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [12-Factor App Principles](https://12factor.net/)
