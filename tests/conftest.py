import pytest
import json
from src.service.app import create_app
from src.service.app import app as flask_app
from flask import url_for
from flask_mongoengine import MongoEngine
from mongoengine import connect


def send_post_data(client, endpoint, data):
    client.post(url_for(endpoint),
                data=json.dumps(data),
                content_type='application/json',
                environ_base={'REMOTE_ADDR': '127.0.0.1'})


@pytest.fixture(scope='session')
def app():

    # db = connect('mongodb')
    # db.drop_database('db_test')
    app = create_app(
        MONGODB_SETTINGS={'db': 'db_test','host':'mongodb'},
        TESTING=True,
        SALT='IfHYBwi5ZUFZD9VaonnK',
    )
    return app
