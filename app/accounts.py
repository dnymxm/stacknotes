from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user

from app import db
from .models import User

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@bp.route('/signup', methods=['GET', 'POST'])
def signup():  # sourcery off
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

        return redirect(url_for('accounts.signin'))

    return render_template('signup.html')


@bp.route('/signin', methods=['GET', 'POST'])
def signin():  # sourcery off
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if not (user and check_password_hash(user.password, password)):
            flash('Please check your login details and try again.')
            return redirect(url_for('accounts.signin'))

        login_user(user)
        return redirect(url_for('notes.index'))

    return render_template('signin.html')


@bp.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('index'))
