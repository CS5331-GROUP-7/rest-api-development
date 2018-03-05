#!/usr/bin/python
# todo:reorder and rearrange
import sys
import datetime
from flask import Flask
from flask_cors import CORS
import json
import os
from flask import request

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_mongoengine import MongoEngine

db = MongoEngine()


def create_app(**config_overrides):
    app = Flask(__name__, static_folder='static', static_url_path='')

    # Load config.
    from views import views
    app.register_blueprint(views)

    # apply overrides
    app.config.update(config_overrides)

    # Setup the database.
    db.init_app(app)

    return app


app = create_app(
    MONGODB_SETTINGS={'db': 'db_deploy', 'host': 'mongodb'},
    TESTING=True,
    SALT='IfHYBwi5ZUFZD9VaonnK',
)
SALT = app.config.get('SALT')
# app.logger.info('here')

'''
todo:move this to separte file
'''


def db_object_to_json(doc):
    ret = {}
    print doc._fields
    # field_dict = doc.get_fields_info()
    for field in doc._fields:
        app.logger.info(field)
        ret[field] = str(doc[field])
    return json.dumps(ret)


def db_object_to_dict(doc):
    ret = {}
    # field_dict = doc.get_fields_info()
    for field in doc._fields:
        app.logger.info(field)
        ret[field] = str(doc[field])
    return ret


class User(db.Document):
    username = db.StringField()
    hashed_password = db.StringField()
    password = db.StringField()
    fullname = db.StringField()
    age = db.IntField()
    registered_date = db.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return db_object_to_json(self)


class Token(db.Document):
    token = db.StringField()
    expiry = db.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))
    isexpired = db.BooleanField()
    data = db.StringField()

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return db_object_to_json(self)


class Diary(db.Document):
    id = db.SequenceField()
    title = db.StringField()
    username = db.StringField()
    published_time = db.StringField()  # ISO8601
    public = db.BooleanField()
    text = db.StringField()

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return db_object_to_json(self)


def is_token_valid(token_str):
    token = Token.objects(token=token_str).first()
    if token is None: return False
    if token.isexpired: return False
    if token.expiry < datetime.datetime.now(): return False

    token_data = json.loads(token.data)
    if request.remote_addr != token_data['ip']: return False
    return True


# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members',
                 '/users', '/users/register', '/users/authenticate', '/users/expire',
                 '/diary', '/diary/create', '/diary/delete', '/diary/permission']

if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    app = create_app(
        MONGODB_SETTINGS={'db': 'db_deploy', 'host': 'mongodb'},
        TESTING=True,
        SALT='IfHYBwi5ZUFZD9VaonnK',
    )

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
