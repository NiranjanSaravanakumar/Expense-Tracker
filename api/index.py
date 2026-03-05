# api/index.py — Vercel Serverless Entry Point
# Vercel looks for a variable named 'app' in this file.

from app import create_app

app = create_app()
