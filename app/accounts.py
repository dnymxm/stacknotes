from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

from app import db
from app import login_manager
from .models import User


bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@bp.route('/signup', methods=['GET', 'POST'])
def signup():  # sourcery off
    """Sign-up form to create new user accounts

    GET: Render Sign-Up page
    POST: Validate form, create account and redirect user to notes dashboard
    """

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists')
            return redirect(url_for('accounts.signup'))

        new_user = User(email=email, password=generate_password_hash(
            password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('notes.index'))

    return render_template('accounts/signup.html')


@bp.route('/signin', methods=['GET', 'POST'])
def signin():  # sourcery off
    """Sign-in form to connect registered users

    GET: Render Sign-In page
    POST: Validate form and redirect user to notes dashboard
    """

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not (user and check_password_hash(user.password, password)):
            flash('Please check your login details and try again.')
            return redirect(url_for('accounts.signin'))

        login_user(user)
        return redirect(url_for('notes.index'))

    return render_template('accounts/signin.html')


@bp.route('/signout')
@login_required
def signout():
    """User log-out logic"""
    logout_user()
    return redirect(url_for('index'))
