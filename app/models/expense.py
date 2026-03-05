"""
Expense model module.
Defines the Expense table for tracking user expenditures.
"""

from datetime import datetime, timezone
from app import db


class Expense(db.Model):
    """
    Expense model representing a single expenditure entry.

    Attributes:
        id: Primary key.
        user_id: Foreign key linking to the owning user.
        amount: Expense amount in currency units.
        category: Category label (e.g., Food, Transport, Entertainment).
        description: Optional description of the expense.
        date: Date the expense occurred.
        created_at: Timestamp of record creation.
    """
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.String(200), default='')
    date = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Available expense categories
    CATEGORIES = [
        'Food & Dining',
        'Transportation',
        'Housing & Rent',
        'Utilities',
        'Entertainment',
        'Shopping',
        'Healthcare',
        'Education',
        'Travel',
        'Personal Care',
        'Subscriptions',
        'Other'
    ]

    def __repr__(self):
        return f'<Expense {self.category}: {self.amount}>'
