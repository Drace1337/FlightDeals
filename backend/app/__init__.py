from flask import Flask
from app.extensions import db

from .config import Config
from .routes.auth import auth_bp
from .routes.search_routes import search_bp,  init_amadeus_service
from .routes.history_routes import history_bp
from .routes.profile_routes import profile_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_login import LoginManager

from .services.amadeus_service import AmadeusService

login_manager = LoginManager()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    
    CORS(app, 
         origins=["http://localhost:3000"],
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         expose_headers=["Content-Type", "Authorization"])
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,X-Requested-With,Accept,Origin')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS,PATCH')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    

    from app.models import User 

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    with app.app_context():
        db.create_all()
        init_amadeus_service(AmadeusService())
    login_manager.login_view = None  

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(search_bp, url_prefix="/search")
    app.register_blueprint(history_bp, url_prefix="/history")
    app.register_blueprint(profile_bp, url_prefix="/profile")

    return app