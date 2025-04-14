from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from flask_migrate import Migrate
from .config import Config
from app.routes.auth import auth_bp
from app.routes.search_routes import search_bp
from app.routes.history_routes import history_bp

db = SQLAlchemy()
# migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(history_bp, url_prefix="/history")

    return app
