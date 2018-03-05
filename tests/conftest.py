import pytest
from src.service.app import create_app
from src.service.app import app as flask_app
from flask_mongoengine import MongoEngine
from mongoengine import connect

@pytest.fixture(scope='session')
def app():

    # db = connect('mongodb')
    # db.drop_database('db_test')
    app=create_app(
            MONGODB_SETTINGS={'db': 'db_test','host':'mongodb'},
        TESTING=True,
        SALT='IfHYBwi5ZUFZD9VaonnK',
    )
    return app
