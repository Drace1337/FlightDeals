from flask import Flask
from app.extensions import db

# from flask_migrate import Migrate
from .config import Config
from app.routes.auth import auth_bp
from app.routes.search_routes import search_bp
from app.routes.history_routes import history_bp
from app.routes.profile_routes import profile_bp
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app.services.amadeus_service import AmadeusService

# migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    # migrate.init_app(app, db)

    from app.models import User 

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    from app.routes.search_routes import init_amadeus_service
    init_amadeus_service(AmadeusService)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(history_bp, url_prefix="/history")
    app.register_blueprint(profile_bp, url_prefix="/profile")

    return app
