import pytest
import json
from src.service.app import create_app
from flask_mongoengine import MongoEngine
from mongoengine import connect




@pytest.fixture(scope='session')
def app():

    # db = connect('mongodb')
    # db.drop_database('db_test')
    # db.close()
    app = create_app(
        MONGODB_SETTINGS={'db': 'db_test','host':'mongodb'},
        TESTING=True,
        SALT='IfHYBwi5ZUFZD9VaonnK',
    )
    return app
