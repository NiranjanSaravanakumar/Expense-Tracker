"""
User model module.
Defines the User table with authentication support via Flask-Login.
"""

from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    """
    User model for authentication and expense ownership.

    Attributes:
        id: Primary key.
        username: Unique username for display.
        email: Unique email address for login.
        password_hash: Werkzeug-hashed password (never stores plain text).
        created_at: Timestamp of account creation.
        expenses: Relationship to the user's expenses.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # One-to-many relationship: a user can have many expenses
    expenses = db.relationship('Expense', backref='owner', lazy='dynamic',
                               cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and store the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader callback."""
    return User.query.get(int(user_id))
