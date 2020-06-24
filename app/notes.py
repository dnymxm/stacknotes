from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from wtforms import TextAreaField

from app import db
from .models import Notes, Tag
from .forms import NoteForm

bp = Blueprint('notes', __name__, url_prefix='/notes')


@bp.route('/')
@login_required
def index():
    notes = Notes.query.filter_by(owner_id=current_user.id).all()
    return render_template('notes/index.html', notes=notes)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():  # sourcery off
    form = NoteForm()
    if form.validate_on_submit():
        note = Notes(title=form.title.data,
                     content=form.content.data,
                     privacy=form.privacy.data,
                     owner_id=current_user.id)
        if form.tags.data:
            tags = form.tags.data.split(', ')
            if tags:
                for tag in tags:
                    tag_exists = Tag.query.filter_by(name=tag).first()
                    if not tag_exists:
                        new_tag = Tag(tag)
                        db.session.add(new_tag)
                        note.tags.append(new_tag)
                    else:
                        db.session.add(tag_exists)
                        note.tags.append(tag_exists)
        db.session.add(note)
        db.session.commit()

        return redirect(url_for('notes.index'))
    return render_template('notes/create.html', form=form)


@bp.route('/view/<int:id>')
def view(id):
    note = Notes.query.get_or_404(id)
    note.visits += 1
    db.session.commit()
    note.owner_id = str(note.owner_id)
    return render_template('notes/view.html', note=note)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    note = Notes.query.get_or_404(id)
    form = NoteForm()

    if request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
        form.privacy.data = note.privacy
        tags = []
        for e in note.tags:
            tag = Tag.query.get_or_404(e.id)
            tags.append(tag.name)
        tags = ', '.join(tags)
        if note.owner_id == current_user.id:
            return render_template('notes/update.html', note=note, tags=tags, form=form)
        else:
            flash("You can't update a page which is not yours", "warning")
            return redirect(url_for('notes.index'))

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        note.privacy = form.privacy.data
        note.updated_at = datetime.now()
        note.tags.clear()
        if form.tags.data:
            tags = form.tags.data.split(', ')
            if tags:
                for tag in tags:
                    tag_exists = Tag.query.filter_by(name=tag).first()
                    if not tag_exists:
                        new_tag = Tag(tag)
                        db.session.add(new_tag)
                        note.tags.append(new_tag)
                    else:
                        db.session.add(tag_exists)
                        note.tags.append(tag_exists)
        db.session.add(note)
        db.session.commit()
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
    notes = Notes.query.filter(Notes.content.like('%'+query+'%'), Notes.privacy.is_(False)).all()
    for note in notes:
        note.owner_id = str(note.owner_id)
    return render_template('notes/search.html', notes=notes)
