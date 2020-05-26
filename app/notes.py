from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from .models import Notes

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/')
@login_required
def index():
    notes = Notes.query.filter_by(owner_id=current_user.id).all()
    return render_template('notes.html', notes=notes, email=current_user.email)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        privacy = False
        owner_id = current_user.id

        note = Notes(title=title, content=content,
                     privacy=privacy, owner_id=owner_id)

        db.session.add(note)
        db.session.commit()

        return redirect(url_for('notes.index'))

    return render_template('create.html')


@bp.route('/view/<int:id>')
def view(id):
    return 'View Note'
