from flask import current_app, Blueprint, request
from models import is_token_valid, User, Token, Diary, db_object_to_dict, db_object_to_json
import datetime
import hashlib
import json
import uuid
from bson import ObjectId

views = Blueprint('views', __name__)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members',
                 '/users', '/users/register', '/users/authenticate', '/users/expire',
                 '/diary', '/diary/create', '/diary/delete', '/diary/permission']


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
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route('/')
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)


@views.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@views.route("/meta/members")
def meta_members():
    team_members = ['Zawlin', 'Xue Si', 'Shi Qing', 'Chen Hui']
    return make_json_response(team_members)


@views.route("/users", methods=['POST'])
def users():
    to_serialize = {'status': False}
    payload = request.get_json()
    if payload and 'token' in payload:
        token_str = payload['token']
    code = 200
    if not is_token_valid(token_str):
        to_serialize['status'] = False
        to_serialize['error'] = 'Invalid authentication token.'
    else:
        token = Token.objects(token=token_str).first()
        data = json.loads(token.data)
        pk = data['pk']
        user = User.objects(pk=ObjectId(pk)).first()
        result = {'username': user.username, 'fullname': user.fullname, 'age': user.age}
        to_serialize['status'] = True
        to_serialize['result'] = json.dumps(result)

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/users/register", methods=['POST'])
def users_register():
    # todo:remove plain text password storage
    #
    # print request.args # for get
    # print request.form # for post
    SALT = current_app.config.get('SALT')
    username, fullname, age, password = None, None, None, None
    payload = request.get_json()
    current_app.logger.info(payload)
    if payload and \
            'password' in payload and \
            'username' in payload and \
            'fullname' in payload and \
            'age' in payload:
        username = payload['username']
        password = payload['password']
        fullname = payload['fullname']
        age = payload['age']
    to_serialize = {'status': False}
    code = 200
    if username is None or fullname is None or age is None or password is None:
        to_serialize['error'] = 'Required parameter is missing'
    elif User.objects(username=username).first() is not None:
        to_serialize['error'] = 'Username already exists'
    else:
        to_serialize['status'] = True
        # note our 'salt' is actually salt+username for extra safety
        hashed_password = hashlib.sha512(password + SALT + username).hexdigest()
        User(username=username, hashed_password=hashed_password, fullname=fullname, age=age).save()
        code = 201

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response
    # return make_json_response(ENDPOINT_LIST)


@views.route("/users/authenticate", methods=['POST'])
def users_authenticate():
    SALT = current_app.config.get('SALT')
    payload = request.get_json()
    username = None
    password = None

    if payload:
        if 'username' in payload:
            username = payload['username']
        if 'password' in payload:
            password = payload['password']

    token = None

    to_serialize = {'status': False}
    code = 200
    if username is None or password is None:
        to_serialize['error'] = 'Required parameter is missing'
    else:
        hashed_password = hashlib.sha512(password + SALT + username).hexdigest()
        user = User.objects(hashed_password=hashed_password).first()  ##????
        if user is not None:
            data = {'pk': str(user.pk), 'ip': request.remote_addr}
            token = Token(token=str(uuid.uuid4()), data=json.dumps(data))
            token.save()

    if token is not None:
        to_serialize['status'] = True
        to_serialize['result'] = {'token': token.token}
    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/users/expire", methods=['POST'])
def users_expire():
    payload = request.get_json()
    if payload and 'token' in payload:
        token_str = payload['token']
    to_serialize = {'status': False}
    code = 200
    if not is_token_valid(token_str):
        to_serialize['status'] = False
    else:
        token = Token.objects(token=token_str).first()
        token.delete()
        to_serialize['status'] = True

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/diary")
def diary():
    to_serialize = {'status': False}
    code = 200
    results = Diary.objects(public=True)
    result = []
    for oneresult in results:
        diary1 = {'id': oneresult.id, 'title': oneresult.title, 'author': oneresult.username,
                  'publish_date': oneresult.published_time, 'public': oneresult.public, 'text': oneresult.text}
        result.append(json.dumps(diary1))
    to_serialize['status'] = True
    to_serialize['result'] = result

    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/diary", methods=['POST'])
def diary_post():
    to_serialize = {'status': False}
    payload = request.get_json()
    if payload:
        token_str = payload['token']
    else:
        token_str = payload
    code = 200
    if is_token_valid(token_str) == False:
        to_serialize['status'] = False
        to_serialize['error'] = 'Invalid authentication token.'
    else:
        token = Token.objects(token=token_str).first()
        data = json.loads(token.data)
        pk = data['pk']
        user = User.objects(pk=ObjectId(pk)).first()
        username = user.username
        results = Diary.objects(username=username)
        result = []
        if results is not None:
            for oneresult in results:
                diary = {'id': oneresult.id, 'title': oneresult.title, 'author': oneresult.username,
                         'publish_date': oneresult.published_time, 'public': oneresult.public, 'text': oneresult.text}
                result.append(json.dumps(diary))
        to_serialize['status'] = True
        to_serialize['result'] = result

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/diary/create", methods=['POST'])
def diary_creation():
    to_serialize = {'status': False}
    title,text,public,token=None,None,None,None
    payload = request.get_json()
    payload2 = request.get_json()
    if payload2 and \
            'title' in payload2 and \
            'text' in payload2 and \
            'public' in payload2:
        title = payload2['title']
        text = payload2['text']
        public = payload2['public']

    if payload:
        token_str = payload['token']
    else:
        token_str = payload
    code = 200
    if is_token_valid(token_str) == False:
        to_serialize['status'] = False
        to_serialize['error'] = 'Invalid authentication token.'
    else:
        if title is None or text is None or public is None:
            to_serialize['error'] = 'Required parameter is missing'
        else:
            token = Token.objects(token=token_str).first()
            data = json.loads(token.data)
            pk = data['pk']
            user = User.objects(pk=ObjectId(pk)).first()
            username = user.username
            dtnow = datetime.datetime.now()
            published_time = dtnow.replace(microsecond=0).isoformat()

            diary = Diary(title=title, username=username, published_time=published_time, public=public, text=text)
            diary.save()
            id=diary.id
            to_serialize['status'] = True
            to_serialize['result'] = {'id': id}

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'

    )
    return response


@views.route("/diary/delete", methods=['POST'])
def diary_delete():
    to_serialize = {'status': False}
    payload = request.get_json()
    payload2 = request.get_json()
    if payload2 and \
            'id' in payload2:
        id = payload2['id']


    if payload:
        token_str = payload['token']
    else:
        token_str = payload
    code = 200
    if is_token_valid(token_str) == False:
        to_serialize['status'] = False
        to_serialize['error'] = 'Invalid authentication token.'
    else:
        if id is None:
            to_serialize['error'] = 'Required parameter is missing'
        else:
            token = Token.objects(token=token_str).first()
            data = json.loads(token.data)
            pk = data['pk']
            user = User.objects(pk=ObjectId(pk)).first()
            username = user.username
            diary = Diary.objects(id=id).first()
            DiaryOwner = diary.username
            if DiaryOwner == username:
                diary.delete()
                to_serialize['status'] = True

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/diary/permission", methods=['POST'])
def diary_permission():
    to_serialize = {'status': False}
    payload = request.get_json()
    payload2 = request.get_json()
    public = payload2['public']
    id = payload2['id']
    payload2 = request.get_json()
    if payload2 and \
            'id' in payload2 and \
            'public' in payload2:

        id = payload2['id']
        public = payload2['public']

    if payload:
        token_str = payload['token']
    else:
        token_str = payload
    code = 200
    if is_token_valid(token_str) == False:
        to_serialize['status'] = False
        to_serialize['error'] = 'Invalid authentication token.'
    else:
        if id is None or public is None:
            to_serialize['error'] = 'Required parameter is missing'
        else:
            token = Token.objects(token=token_str).first()
            data = json.loads(token.data)
            pk = data['pk']
            user = User.objects(pk=ObjectId(pk)).first()
            username = user.username
            diary = Diary.objects(id=id).first()
            DiaryOwner = diary.username
            if DiaryOwner == username:
                diary.update(public=public)
                to_serialize['status'] = True

    # todo make the json_response() better
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/debug/resetdb")
def debug_resetdb():
    to_serialize = {'status': 'success'}
    User.drop_collection()
    Token.drop_collection()
    Diary.drop_collection()
    code = 200
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response


@views.route("/debug/rawdb")
def debug_getrawdb():
    to_serialize = {'status': 'success'}
    to_serialize['users'] = [db_object_to_dict(usr) for usr in User.objects()]
    to_serialize['tokens'] = [db_object_to_dict(token) for token in Token.objects()]
    to_serialize['diaries'] = [db_object_to_dict(diary) for diary in Diary.objects()]
    code = 200
    response = current_app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response
