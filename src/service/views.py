from flask import current_app, Blueprint
import json

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
