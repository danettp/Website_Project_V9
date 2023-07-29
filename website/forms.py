from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

# Registration form for user sign up
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    # Validation to check if the username is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That Username is already taken. Please choose a different one.')
    
    # Validation to check if the email is already taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')
        
# Update Account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed('jpg', 'png')])
    submit = SubmitField('Update')
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    
    def validate_username(self, username):
        # Custom validation for the username field
        if username.data !=current_user.username:
            # Check if the entered username is different from the current user's username
            user = User.query.filter_by(username=username.data).first() 
            # Query the database to check if another user already has the same username
            if user:
                # If a user with the entered username already exists, raise a validation error
                raise ValidationError('That Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data !=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                # If a user with the entered email already exists, raise a validation error
                raise ValidationError('That email is already taken. Please choose a different one.')
            
# Custom validator for word count
def word_count_check(form, field):
    min_words = 5  # Minimum number of words allowed
    max_words = 100  # Maximum number of words allowed

    # Count the number of words in the field's input
    word_count = len(field.data.split())

    if word_count < min_words:
        raise ValidationError(f'Text must have at least {5} words.')

    if word_count > max_words:
        raise ValidationError(f'You have reached the maximum of {500} words.')

# Post Form
class PostForm(FlaskForm):
    # Title of post
    title = StringField('Title', validators=[DataRequired()])
    # Content of posts
    text = TextAreaField('Text', validators=[DataRequired(), word_count_check])
    # Submit Post Button
    submit = SubmitField('Update')