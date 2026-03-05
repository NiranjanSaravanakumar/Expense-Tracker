"""
Expense routes blueprint.
Handles CRUD operations for expenses, filtering, and monthly reports.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense
from app.forms import ExpenseForm
from app.services.expense_service import ExpenseService

expense_bp = Blueprint('expenses', __name__, url_prefix='/expenses')


@expense_bp.route('/')
@login_required
def list_expenses():
    """
    Display all expenses for the current user with optional filters.
    Supports filtering by category, month, and year via query params.
    """
    # Get filter parameters from query string
    category = request.args.get('category', '')
    month = request.args.get('month', '')
    year = request.args.get('year', '')

    expenses = ExpenseService.get_filtered_expenses(
        user_id=current_user.id,
        category=category if category else None,
        month=month if month else None,
        year=year if year else None
    )

    return render_template(
        'expenses/list.html',
        expenses=expenses,
        categories=Expense.CATEGORIES,
        selected_category=category,
        selected_month=month,
        selected_year=year
    )


@expense_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add a new expense for the current user."""
    form = ExpenseForm()

    if form.validate_on_submit():
        expense = Expense(
            user_id=current_user.id,
            amount=round(form.amount.data, 2),
            category=form.category.data,
            description=form.description.data.strip() if form.description.data else '',
            date=form.date.data
        )
        db.session.add(expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('expenses.list_expenses'))

    return render_template('expenses/add.html', form=form)


@expense_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit an existing expense. Only the owner can edit."""
    expense = Expense.query.get_or_404(expense_id)

    # Ensure the expense belongs to the current user
    if expense.user_id != current_user.id:
        abort(403)

    form = ExpenseForm(obj=expense)

    if form.validate_on_submit():
        expense.amount = round(form.amount.data, 2)
        expense.category = form.category.data
        expense.description = form.description.data.strip() if form.description.data else ''
        expense.date = form.date.data

        db.session.commit()

        flash('Expense updated successfully!', 'success')
        return redirect(url_for('expenses.list_expenses'))

    return render_template('expenses/edit.html', form=form, expense=expense)


@expense_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete an expense. Only the owner can delete."""
    expense = Expense.query.get_or_404(expense_id)

    # Ensure the expense belongs to the current user
    if expense.user_id != current_user.id:
        abort(403)

    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted successfully!', 'success')
    return redirect(url_for('expenses.list_expenses'))


@expense_bp.route('/report')
@login_required
def monthly_report():
    """
    Display the monthly expense report.
    Accepts optional month and year query parameters.
    """
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)

    month = request.args.get('month', now.month, type=int)
    year = request.args.get('year', now.year, type=int)

    report = ExpenseService.get_monthly_report(current_user.id, year, month)

    return render_template('expenses/report.html', report=report)
