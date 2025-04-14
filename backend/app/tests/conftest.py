import pytest
from app import create_app
from app.extensions import db
from app.config import TestConfig
from flask_jwt_extended import create_access_token
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)


@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers():
    token = create_access_token(identity=1)  # Assuming user ID 1 for testing
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
