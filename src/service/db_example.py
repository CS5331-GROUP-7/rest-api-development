# -*- coding: utf-8 -*-
import os
import sys
import datetime
import flask
import bson
import uuid
import json

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
    uid = db.SequenceField()
    name =  db.StringField()
    password = db.StringField()
    registered_date = db.DateTimeField(default=datetime.datetime.now)

    def __repr__(self):
        return 'id=%s, data = [%s:%s]'%(self.pk,self.name,self.password)

class Token(db.Document):
    token = db.StringField()
    expiry = db.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=1))
    isexpired = db.BooleanField()
    data = db.StringField()
    def __repr__(self):
        return 'token=%s, data = [%s]'%(self.token,self.data)

class Counter(db.Document):
    count = db.IntField()
    def __repr__(self):
        return 'counter = %d'%(self.count)



# insert
def test_insert():
    count = Counter(count=0)
    count.save()
    dtnow = datetime.datetime.now()
    print dtnow.isoformat()

    user = User(name='TestUser',password='asdf')
    user.save()

    user = User(name='TestUser2',password='asdf')
    user.save()

    user = User(name='TestUser3',password='asdf')
    user.save()

    data = {'pk':str(user.pk),'ip':'127.0.0.1'}
    token = Token(token=str(uuid.uuid4()),data =  json.dumps(data))
    token.save()

    data2 = {'pk':str(user.pk),'ip':'127.0.0.1'}
    token = Token(token=str(uuid.uuid4()),data =  json.dumps(data2))
    token.save()

    data3 = {'pk':str(user.pk),'ip':'127.0.0.1'}
    token = Token(token=str(uuid.uuid4()),data =  json.dumps(data3))
    token.save()

    count = Counter.objects()[0]
    count1 = count.count + 1
    count.update(count=count1)



def test_update():
    objs = User.objects(name='TestUser2')
    objs[0].update(name='testchanged')

    obj = User.objects(name='TestUser3').first()
    obj.update(name='testchanged3')

def test_delete():
    objs=User.objects(name='TestUser')
    objs[0].delete()

def test_searchby_pk():
    pk = User.objects()[0].pk
    print User.objects(pk=pk)
User.drop_collection()#clear all User collection
test_insert()
print User.objects()
results = Token.objects()
for result in results:
    print result.token
print Counter.objects()
#test_update()
#print User.objects()
#test_delete()
#print User.objects()
#test_searchby_pk()

