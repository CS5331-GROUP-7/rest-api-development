import pytest
import json
from flask import url_for
from src.service.app import User
import urllib2


from flask_mongoengine import MongoEngine
from mongoengine import connect
@pytest.mark.usefixtures('client_class')
class TestUsersEmpty(object):

    @classmethod
    def setup_class(self):

        pass
        # db = connect('mongodb')
        # db.drop_database('db_test')
        #code = 200
        #res = urllib2.urlopen('http://app:8080/debug/resetdb')

        #assert 'success' in res.read()
        #assert res.code == 200


    @classmethod
    def teardown_class(self):
        pass

    def test_users_no_token(self):
        response = self.client.post(url_for('users'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_users_invalid_token(self):
        response = self.client.post(url_for('users'), data=dict(token="b563fdc7-1c1c-46d8-a7a0-42ea1f1d9c4d"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_user_register_no_args(self):
        response = self.client.post(url_for('users_register'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_register_no_username(self):
        response = self.client.post(url_for('users_register'), data=dict(password="2", fullname="3", age="4"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_register_no_password(self):
        response = self.client.post(url_for('users_register'), data=dict(username="1", fullname="3", age="4"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_register_no_fullname(self):
        response = self.client.post(url_for('users_register'), data=dict(username="1", password="2", age="4"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_register_no_age(self):
        response = self.client.post(url_for('users_register'), data=dict(username="1", password="2", fullname="3"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_register_success(self):
        response = self.client.post(url_for('users_register'),
                                    data=dict(username="1", password="2", fullname="3", age="4"))
        assert response.status_code == 201

        data = json.loads(response.data)
        assert 'error' not in data
        assert 'status' in data

        assert data['status']

        # delete user
        user = User.objects(username="1").first()
        user.delete()
        assert not User.objects(username="1").first()

    def test_user_authenticate_no_args(self):
        response = self.client.post(url_for('users_authenticate'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_authenticate_no_username(self):
        response = self.client.post(url_for('users_authenticate'), data=dict(password="2"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_authenticate_no_password(self):
        response = self.client.post(url_for('users_authenticate'), data=dict(username="1"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Required parameter is missing' in data['error']

    def test_user_authenticate_valid_args_no_token(self):
        response = self.client.post(url_for('users_authenticate'), data=dict(username="1", password="2"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' not in data
        assert 'status' in data

        assert not data['status']

    def test_users_expire_no_token(self):
        response = self.client.post(url_for('users_expire'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' not in data
        assert 'status' in data

        assert not data['status']

    def test_users_expire_invalid_token(self):
        response = self.client.post(url_for('users_expire'), data=dict(token="b563fdc7-1c1c-46d8-a7a0-42ea1f1d9c4d"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' not in data
        assert 'status' in data

        assert not data['status']


if __name__ == '__main__':
    pytest.main()
