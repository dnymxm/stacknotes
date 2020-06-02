from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown

db = SQLAlchemy()
migrate = Migrate()
mde = SimpleMDE()


def create_app(config_file='config.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'accounts.signin'
    login_manager.init_app(app)
    mde.init_app(app)
    Markdown(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('notes.index'))
        return render_template('index.html')

    from . import notes
    app.register_blueprint(notes.bp)

    from . import accounts
    app.register_blueprint(accounts.bp)

    return app
