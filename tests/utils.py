import json


def send_post_data(client, endpoint, data):
    return client.post(endpoint,
                data=json.dumps(data),
                content_type='application/json',
                environ_base={'REMOTE_ADDR': '127.0.0.1'})


def send_post(client, endpoint):
    return client.post(endpoint,
                content_type='application/json',
                environ_base={'REMOTE_ADDR': '127.0.0.1'})
