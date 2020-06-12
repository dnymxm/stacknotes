from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), primary_key=True),
                db.Column('notes_id', db.Integer, db.ForeignKey(
                    'notes.id'), primary_key=True)
                )


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=None)
    content = db.Column(db.String(300), nullable=None)
    privacy = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    visits = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('notes', lazy=True))

    def __repr__(self):
        return f"<Notes - Title: {self.title} | Owner ID: {self.owner_id} | Visits: {self.visits}>"


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=None)
    email = db.Column(db.String(120), index=True, unique=True, nullable=None)
    password = db.Column(db.String(128))
    website = db.Column(db.String(120))
    notes = db.relationship('Notes', backref='owner')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.email}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=None)

    def __init__(self, name):
        self.name = name
