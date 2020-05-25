from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app import db
from .models import Notes

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/')
@login_required
def index():
    notes = Notes.query.all()
    return render_template('notes.html', notes=notes, email=current_user.email)


@bp.route('/create')
def create():
    return 'Create Note'


@bp.route('/view/<int:id>')
def view(id):
    return 'View Note'
