
from app.extensions import db
from app import create_app
from unittest.mock import patch
import pytest
import os

# говорим приложению использовать TestingConfig (in-memory SQLite)
os.environ['FLASK_ENV'] = 'testing'


@pytest.fixture
def app():

    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def mock_publish():

    # отключаем реальную публикацию в RabbitMQ
    with patch('app.api.notifications.publish_notification') as m:
        yield m
