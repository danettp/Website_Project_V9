"""Does forms for Flask web application."""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField,
    validators
)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo, ValidationError
)
from .models import User


# Registration form for user sign up
class RegistrationForm(FlaskForm):
    """Form to handle user registration and sign up."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), Length(min=8),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Custom validation for taken usernames."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is already taken. '
                                  'Please choose a different one.')

    def validate_email(self, email):
        """Custom validation to check if the email is already taken."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. '
                                  'Please choose a different one.')


# Update Account form
class UpdateAccountForm(FlaskForm):
    """Form to handle updating user account details."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture',
                        validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """Validate username."""

        if username.data !=current_user.username:
            # Check if username is different from current username
            user = User.query.filter_by(username=username.data).first()
            # Query the database if username is the same
            if user:
                # Raise a validation error if username exists
                raise ValidationError('That Username is already taken. '
                                      'Please choose a different one.')

    def validate_email(self, email):
        if email.data !=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                # Raise a validation error if email exists
                raise ValidationError('That email is already taken. '
                                      'Please choose a different one.')

# Post Form
class PostForm(FlaskForm):
    """Form to handle creating and updating posts."""

    title = StringField('Title', validators=[DataRequired()])
    # Content of posts
    text = TextAreaField('Text', validators=[DataRequired(), Length(min=5, max=1000)])
    # Submit Post Button
    submit = SubmitField('Update')
