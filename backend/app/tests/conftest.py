import pytest
from app import create_app
from app.extensions import db
from app.config import TestConfig
from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
from sqlalchemy.orm import close_all_sessions
import logging
from app.routes.search_routes import init_amadeus_service
from app.services.amadeus_service import AmadeusService

load_dotenv()
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def app():
    """Fixture to create a Flask application instance for testing."""
    app = create_app(config_class=TestConfig)
    with app.app_context():
        init_amadeus_service(AmadeusService())
        db.create_all()
        yield app
        db.session.remove()
        close_all_sessions()
        db.drop_all()
        db.engine.dispose()



@pytest.fixture
def client(app):
    """Fixture to create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def auth_headers():
    """Fixture to create authentication headers for testing."""
    token = create_access_token(identity=str(1))  
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


