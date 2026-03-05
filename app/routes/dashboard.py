"""
Dashboard routes blueprint.
Provides the main dashboard view and the JSON API for chart data.
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.services.expense_service import ExpenseService

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@login_required
def index():
    """
    Main dashboard page.
    Shows total monthly expense and category breakdown with Chart.js pie chart.
    """
    report = ExpenseService.get_monthly_report(current_user.id)

    return render_template('dashboard/index.html', report=report)


@dashboard_bp.route('/api/chart-data')
@login_required
def chart_data():
    """
    REST API endpoint returning category-wise expense data in JSON.
    Used by the Chart.js frontend to render the pie chart.

    Returns:
        JSON: {
            "labels": ["Food & Dining", "Transport", ...],
            "values": [150.00, 80.50, ...],
            "total": 450.50,
            "month": 3,
            "year": 2026
        }
    """
    report = ExpenseService.get_monthly_report(current_user.id)

    return jsonify({
        'labels': [item['category'] for item in report['breakdown']],
        'values': [item['amount'] for item in report['breakdown']],
        'total': report['total'],
        'month': report['month'],
        'year': report['year']
    })
