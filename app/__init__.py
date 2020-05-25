from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_file='config.py'):

    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'accounts.signin'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return render_template('index.html')

    from . import notes
    app.register_blueprint(notes.bp)

    from . import accounts
    app.register_blueprint(accounts.bp)

    return app
