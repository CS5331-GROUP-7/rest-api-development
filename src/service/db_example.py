# -*- coding: utf-8 -*-
import os
import sys
import datetime
import flask

sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_mongoengine import MongoEngine

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'DB': 'db_test'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
db = MongoEngine()
db.init_app(app)


class User(db.Document):
    name =  db.StringField()
    password = db.StringField()
    registered_date = db.DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return '%s:%s'%(self.name,self.password)

class Token(db.Document):
    expiry = db.DateTimeField(default=datetime.datetime.now)


# insert
def test_insert():
    user = User(name='TestUser',password='asdf')
    user.save()

    user = User(name='TestUser2',password='asdf')
    user.save()

    user = User(name='TestUser3',password='asdf')
    user.save()


def test_update():
    objs = User.objects(name='TestUser2')
    objs[0].update(name='testchanged')

    obj = User.objects(name='TestUser3').first()
    obj.update(name='testchanged3')

def test_delete():
    objs=User.objects(name='TestUser')
    objs[0].delete()

User.drop_collection()#clear all User collection
test_insert()
print User.objects()
test_update()
print User.objects()
test_delete()
print User.objects()
print User.objects(name='dfdf').first()

