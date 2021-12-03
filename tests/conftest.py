import pytest
from flask import Flask
from models import db


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
        yield client
