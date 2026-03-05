"""
Flask application factory module.
Initializes extensions and registers blueprints.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions (created here, bound to app in create_app)
db = SQLAlchemy()
login_manager = LoginManager()

# Configure login manager defaults
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'


def format_inr(value):
    """
    Jinja2 custom filter: formats a number using Indian comma grouping.
    e.g.  150.5     -> "150.50"
          12197.0   -> "12,197.00"
          100000.0  -> "1,00,000.00"
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    # Split into integer and decimal parts
    integer_part = int(value)
    decimal_part = round((value - integer_part) * 100)

    # Indian grouping: last 3 digits, then groups of 2 from right
    s = str(integer_part)
    if len(s) <= 3:
        formatted_int = s
    else:
        formatted_int = s[-3:]
        s = s[:-3]
        while s:
            formatted_int = s[-2:] + ',' + formatted_int
            s = s[:-2]

    return f"{formatted_int}.{decimal_part:02d}"


def create_app():
    """
    Application factory function.
    Creates and configures the Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Register custom Jinja2 filters
    app.jinja_env.filters['format_inr'] = format_inr

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.expense import expense_bp
    from app.routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)
    app.register_blueprint(dashboard_bp)

    # Create database tables on first request
    with app.app_context():
        from app.models import user, expense  # noqa: F401
        db.create_all()

    return app
