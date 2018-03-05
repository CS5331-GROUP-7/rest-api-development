from flask import current_app, request
from app import db
import datetime
import json


def is_token_valid(token_str):
    token = Token.objects(token=token_str).first()
    if token is None: return False
    if token.isexpired: return False
    if token.expiry < datetime.datetime.now(): return False

    token_data = json.loads(token.data)
    if request.remote_addr != token_data['ip']: return False
    return True


def db_object_to_json(doc):
    ret = {}
    print doc._fields
    # field_dict = doc.get_fields_info()
    for field in doc._fields:
        current_app.logger.info(field)
        ret[field] = str(doc[field])
    return json.dumps(ret)


def db_object_to_dict(doc):
    ret = {}
    # field_dict = doc.get_fields_info()
    for field in doc._fields:
        current_app.logger.info(field)
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
    id = db.SequenceField(primary_key=True)
    title = db.StringField()
    username = db.StringField()
    published_time = db.StringField()  # ISO8601
    public = db.BooleanField()
    text = db.StringField()

    def __str__(self):
        return self.__repr__();

    def __repr__(self):
        return db_object_to_json(self)
