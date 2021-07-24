from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate = Migrate(app, db)

    with app.app_context():
        from .models import hitman, hit, managers_lackeys
        from .views import hitman_view, hit_view

        return app
