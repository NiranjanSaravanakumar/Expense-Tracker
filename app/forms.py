"""
WTForms form definitions.
Provides server-side validation for all user inputs.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, FloatField,
    SelectField, TextAreaField, DateField, SubmitField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length,
    NumberRange, ValidationError
)
from app.models.user import User
from app.models.expense import Expense


class RegistrationForm(FlaskForm):
    """User registration form with validation."""

    username = StringField('Username', validators=[
        DataRequired(message='Username is required.'),
        Length(min=3, max=80, message='Username must be 3–80 characters.')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords do not match.')
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        """Check that the username is not already taken."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):
        """Check that the email is not already registered."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')


class LoginForm(FlaskForm):
    """User login form."""

    email = StringField('Email', validators=[
        DataRequired(message='Email is required.'),
        Email(message='Please enter a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.')
    ])
    submit = SubmitField('Log In')


class ExpenseForm(FlaskForm):
    """Form for adding or editing an expense."""

    amount = FloatField('Amount', validators=[
        DataRequired(message='Amount is required.'),
        NumberRange(min=0.01, message='Amount must be greater than zero.')
    ])
    category = SelectField('Category', validators=[
        DataRequired(message='Please select a category.')
    ])
    description = TextAreaField('Description', validators=[
        Length(max=200, message='Description must be under 200 characters.')
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[
        DataRequired(message='Date is required.')
    ])
    submit = SubmitField('Save Expense')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate category choices from the Expense model constant
        self.category.choices = [(c, c) for c in Expense.CATEGORIES]
