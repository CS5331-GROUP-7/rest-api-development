import json
from flask import url_for

def send_post_data(client, endpoint, data):
    return client.post(url_for(endpoint),
                data=json.dumps(data),
                content_type='application/json',
                environ_base={'REMOTE_ADDR': '127.0.0.1'})
