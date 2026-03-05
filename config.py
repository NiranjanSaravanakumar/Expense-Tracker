"""
Application configuration module.
Loads settings from environment variables via .env file.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""

    # Flask secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///expense_tracker.db')

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # WTForms CSRF protection
    WTF_CSRF_ENABLED = True
