import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message
from is_safe_url import is_safe_url
from app import db, login_manager, mail
from .models import User
from .forms import SignupForm, SigninForm, ResetPasswordRequestForm, ResetPasswordForm
from .email import send_password_reset_email

bp = Blueprint('accounts', __name__, url_prefix='/accounts')


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Sign-up form to create new user accounts

    GET: Render Sign-Up page
    POST: Validate form, create account and redirect user to notes dashboard
    """
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            new_user = User(name=form.name.data,
                            email=form.email.data,
                            website=form.website.data
                            )
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Your account has been created ✌️', 'primary')
            return redirect(url_for('notes.index'))
        flash('Email address already exists', 'info')
    return render_template('accounts/signup.html', form=form)


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    """Sign-in form to connect registered users

    GET: Render Sign-In page
    POST: Validate form and redirect user to notes dashboard or the page he wanteed to access

    Protected against open redirectories with is_safe_url()
    """
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))

    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and user.check_password(password=form.password.data)):
            login_user(user)
            if request.args:
                next_page = request.args.get('next')
                id = request.args.get('id')
                if is_safe_url(url=next_page, allowed_hosts=request.host_url):
                    return redirect(url_for(next_page, id=id))
            return redirect(url_for('notes.index'))
        flash('Please check your login details and try again.', 'warning')
        return redirect(url_for('accounts.signin'))
    return render_template('accounts/signin.html', form=form)


@bp.route('/signout')
@login_required
def signout():
    """User log-out logic"""
    logout_user()
    return redirect(url_for('index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Reset Password Request"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash(
                'Check your email for the instructions to reset your password', 'primary')
            return redirect(url_for('accounts.signin'))
    return render_template('accounts/reset_password_request.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset Password"""
    if current_user.is_authenticated:
        return redirect(url_for('notes.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'primary')
        return redirect(url_for('accounts.signin'))
    return render_template('accounts/reset_password.html', form=form, token=token)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login or Index page."""
    if request.endpoint == 'accounts.signout':
        return redirect(url_for('index'))
    flash('You must be logged in to view that page.', 'info')
    return redirect(url_for('accounts.signin', next=request.endpoint, **request.view_args))
