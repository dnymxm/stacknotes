from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import db
from .models import Notes

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/')
@login_required
def index():
    notes = Notes.query.filter_by(owner_id=current_user.id).all()
    return render_template('notes/index.html', notes=notes)


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
    return render_template('notes/create.html')


@bp.route('/view/<int:id>')
def view(id):
    note = Notes.query.get_or_404(id)
    note.owner_id = str(note.owner_id)
    return render_template('notes/view.html', note=note)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    note = Notes.query.get_or_404(id)
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('notes.index'))
    else:
        if note.owner_id == int(current_user.get_id()):
            return render_template('notes/update.html', note=note)
        else:
            flash("You can't update a page which is not yours", "error")
            return redirect(url_for('notes.index'))


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    note = Notes.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('notes.index'))


@bp.route('/search')
@login_required
def search():
    query = request.args.get('q')
    notes = Notes.query.filter(Notes.content.like('%'+query+'%')).all()
    for note in notes:
        note.owner_id = str(note.owner_id)
    return render_template('notes/search.html', notes=notes)
