from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import RegistrationForm

auth = Blueprint("auth", __name__)

# Login route for user authentication
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password): # Check if the provided password matches the hashed password stored in the database
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Sign up route for user registration
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash((form.password.data), method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) # Create a new User object with the provided data
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form, user=current_user)

# Logout route for user log out       
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))