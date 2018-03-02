#!/usr/bin/python
# todo:reorder and rearrange
import sys
import datetime
import os
from flask import Flask
from flask_cors import CORS
import json
import os
from flask_mongoengine import MongoEngine
import uuid
import flask
from flask import request
import hashlib
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '../../')))

from flask_mongoengine import MongoEngine

app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config['MONGODB_SETTINGS'] = {'db': 'db_test',
                                  'host':'mongodb'}
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'flask+mongoengine=<3'
app.debug = True
db = MongoEngine()
db.init_app(app)
SALT =  'IfHYBwi5ZUFZD9VaonnK'
id = 0
'''
todo:move this to separte file
'''

class User(db.Document):
    username=  db.StringField()
    hashed_password = db.StringField()
    password = db.StringField()
    fullname= db.StringField()
    age= db.IntField()
    registered_date = db.DateTimeField(default=datetime.datetime.now)


    def __str__(self):
        return self.__repr__();
    def __repr__(self):
        return '%s:%s'%(self.username,self.hashed_password)

class Token(db.Document):
    token = db.StringField()
    expiry = db.DateTimeField(default=datetime.datetime.now()+datetime.timedelta(days=1))
    isexpired = db.BooleanField()
    data = db.StringField()

    def __str__(self):
        return self.__repr__();
    def __repr__(self):
        return '%s'%(self.expiry)

class Diary(db.Document):
	userid = db.StringField()
	title = db.BooleanField()
	public = db.StringField()
	text = db.StringField()
	id = db.IntField(primary_key=True)


def is_token_valid(token_str):
    token = Token.objects(token=token_str).first()
    if token is None:return False
    if token.isexpired:return False
    if token.expiry<datetime.datetime.now():return False

    token_data = json.loads(token.data)
    if request.remote_addr != token_data['ip']:return False
    return True

app = Flask(__name__)
# Enable cross origin sharing for all endpoints
CORS(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members']

def make_json_response(data, status=True, code=200):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
    else:
        to_serialize['status'] = False
        to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@app.route("/")
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)

@app.route("/users")
def user_page():
    userobjs = [str(obj) for obj in User.objects()]
    return make_json_response(userobjs)

@app.route("/users/register",methods=['POST'])
def users_register():
    #todo:remove plain text password storage
    #
    #print request.args # for get
    #print request.form # for post
    username,fullname,age,password =  None,None,None,None
    username = request.form.get('username')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    age  = request.form.get('age')
    to_serialize={'status':False}
    code = 200
    if username is None or fullname is None or age is None or password is None:
        to_serialize['error'] = 'Required parameter is missing'
    elif User.objects(username = username).first() is not None:
        to_serialize['error'] = 'Username already exists'
    else:
        to_serialize['status']=True
        # note our 'salt' is actually salt+username for extra safety
        hashed_password = hashlib.sha512(password + SALT+username).hexdigest()
        User(username = username,hashed_password=hashed_password,fullname=fullname,age=age).save()
        code = 201


    #todo make the json_response() better
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response
    #return make_json_response(ENDPOINT_LIST)

@app.route("/users/authenticate",methods=['POST'])
def users_authenticate():
    username = request.form.get('username')
    password = request.form.get('password')


    hashed_password = hashlib.sha512(password + SALT+username).hexdigest()
    token = None
    user = User.objects(hashed_password=hashed_password).first()
    if  user is not None:
        data = {'pk':str(user.s),'ip':request.remote_addr}
        token = Token(token=str(uuid.uuid4()),data =  json.dumps(data))
        token.save()

    to_serialize={'status':False}
    code = 200
    if username is None or password is None:
        to_serialize['error'] = 'Required parameter is missing'
    elif token is  not None:
        to_serialize['status']=True
        to_serialize['token'] = token.token
    #todo make the json_response() better
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'

    )
    return response

@app.route("/diary/create",methods=['POST'])
def diary_creation():
    token = request.form.get('token')
    #if is_token_valid(token) == False:
    #	code = 201
    #	to_serialize['status'] = False
    #	to_serialize['error'] = 'Invalid authentication token.'
    if True:
    	code = 200
    	userid = token[0].data.pk
    	title = request.form.get('title')
    	text = request.form.get('text')
    	public = request.form.get('public')
    	id = id + 1
    	Diary( userid= userid,title=title,text=text,public=public,id=id).save()
    	to_serialize['status'] = True
    	to_serialize['id'] = id

    #todo make the json_response() better
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'

    )
    return response


@app.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@app.route("/meta/members")
def meta_members():
    team_members = ['Zawlin','Xue Xi','ShiQing','ChenHui']
    return make_json_response(team_members)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Run the application
    app.run(debug=False, port=8080, host="0.0.0.0")
