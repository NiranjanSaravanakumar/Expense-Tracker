"""
Expense service module.
Contains business logic for expense aggregation, filtering, and reporting.
"""

from datetime import datetime, timezone
from sqlalchemy import func, extract
from app import db
from app.models.expense import Expense


class ExpenseService:
    """Service class encapsulating expense-related business logic."""

    @staticmethod
    def get_monthly_total(user_id, year=None, month=None):
        """
        Calculate the total expense amount for a given month.

        Args:
            user_id: The authenticated user's ID.
            year: Target year (defaults to current year).
            month: Target month (defaults to current month).

        Returns:
            Float total of expenses for the specified month.
        """
        now = datetime.now(timezone.utc)
        year = year or now.year
        month = month or now.month

        result = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).scalar()

        return result or 0.0

    @staticmethod
    def get_category_breakdown(user_id, year=None, month=None):
        """
        Get expense totals grouped by category for a given month.

        Args:
            user_id: The authenticated user's ID.
            year: Target year (defaults to current year).
            month: Target month (defaults to current month).

        Returns:
            List of tuples: [(category, total_amount), ...]
        """
        now = datetime.now(timezone.utc)
        year = year or now.year
        month = month or now.month

        results = db.session.query(
            Expense.category,
            func.sum(Expense.amount).label('total')
        ).filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).all()

        return results

    @staticmethod
    def get_filtered_expenses(user_id, category=None, month=None, year=None):
        """
        Retrieve expenses with optional category and date filters.

        Args:
            user_id: The authenticated user's ID.
            category: Optional category filter.
            month: Optional month filter.
            year: Optional year filter.

        Returns:
            List of Expense objects matching the filters.
        """
        query = Expense.query.filter_by(user_id=user_id)

        if category:
            query = query.filter(Expense.category == category)

        if month and year:
            query = query.filter(
                extract('year', Expense.date) == int(year),
                extract('month', Expense.date) == int(month)
            )

        return query.order_by(Expense.date.desc()).all()

    @staticmethod
    def get_monthly_report(user_id, year=None, month=None):
        """
        Generate a comprehensive monthly expense report.

        Args:
            user_id: The authenticated user's ID.
            year: Target year (defaults to current year).
            month: Target month (defaults to current month).

        Returns:
            Dictionary containing total, breakdown, and expense count.
        """
        now = datetime.now(timezone.utc)
        year = year or now.year
        month = month or now.month

        total = ExpenseService.get_monthly_total(user_id, year, month)
        breakdown = ExpenseService.get_category_breakdown(user_id, year, month)

        # Count of transactions this month
        count = Expense.query.filter(
            Expense.user_id == user_id,
            extract('year', Expense.date) == year,
            extract('month', Expense.date) == month
        ).count()

        return {
            'total': round(total, 2),
            'breakdown': [{'category': cat, 'amount': round(amt, 2)} for cat, amt in breakdown],
            'count': count,
            'year': year,
            'month': month
        }
