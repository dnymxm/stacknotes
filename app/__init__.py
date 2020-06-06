from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_simplemde import SimpleMDE
from flaskext.markdown import Markdown

db = SQLAlchemy()
migrate = Migrate()
mde = SimpleMDE()
login_manager = LoginManager()


def create_app(config_file='config.py'):
    """Construct the core app object"""
    app = Flask(__name__)

    # Application Configuration
    app.config.from_pyfile(config_file)

    # Initialize extensions
    # Database
    db.init_app(app)
    # Migrations
    migrate.init_app(app, db)
    # View by default for unauthorized users
    login_manager.login_view = 'accounts.signin'
    # Authentification
    login_manager.init_app(app)
    # Mardkown Editor
    mde.init_app(app)
    # Markdown Renderer
    Markdown(
        app,
        extensions=['fenced_code', 'codehilite'],
        extension_configs={'codehilite': {
            'noclasses': True,
            'pygments_style': 'friendly'}
        }
    )

    # Landing page
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('notes.index'))
        return render_template('index.html')

    # Register Blueprints
    from . import notes
    app.register_blueprint(notes.bp)

    from . import accounts
    app.register_blueprint(accounts.bp)

    return app
