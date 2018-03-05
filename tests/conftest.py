import pytest
from src.service.app import app as flask_app

@pytest.fixture(scope='session')
def app():
    return flask_app
