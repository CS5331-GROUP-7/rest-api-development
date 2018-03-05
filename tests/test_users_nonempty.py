import pytest
import json
import hashlib
from flask import url_for
from src.service.app import SALT
from src.service.models import User, Token, is_token_valid

user1 = "user1"
user1pw = "password1"
user1name = "user1"
user1age = "1"
token1uuid = "f7d86d6c-2c13-47b2-8d45-3da9cf943fc9"
expired_token = "e7326198-7055-4559-8d2b-b4568855211e"
localhost = '127.0.0.1'


@pytest.mark.usefixtures('client_class')
class TestUsersNonEmpty(object):
    @classmethod
    def setup_class(cls):
        hash_password = hashlib.sha512(user1pw + SALT + user1).hexdigest()
        User(username=user1, hashed_password=hash_password, fullname=user1name, age=user1age).save()
        user = User.objects(username=user1).first()
        userid = str(user.pk)

        data = {'pk': userid, 'ip': localhost}
        token = Token(token=token1uuid, data=json.dumps(data))
        token.save()

        token = Token(token=expired_token, data=json.dumps(data), isexpired=True)
        token.save()

    @classmethod
    def teardown_class(cls):
        user = User.objects(username=user1).first()
        user.delete()

        token = Token.objects(token=token1uuid).first()
        if token:
            token.delete()

        token = Token.objects(token=expired_token).first()
        if token:
            token.delete()

    def test_users_valid_token(self):
        response = self.client.post(url_for('views.users'),
                                    data=dict(token=token1uuid),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'result' in data
        assert 'status' in data

        assert data['status']
        user_data = json.loads(data['result'])
        assert user_data['username'] == user1
        assert user_data['fullname'] == user1name
        assert user_data['age'] == int(user1age)

    def test_users_register_username_exist(self):
        response = self.client.post(url_for('views.users_register'),
                                    data=dict(username=user1, password="2", fullname="3", age="4"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Username already exists' in data['error']

    def test_users_authenticate_success(self):
        response = self.client.post(url_for('views.users_authenticate'), data=dict(username=user1, password=user1pw,fullname=user1name,age=user1age))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert 'result' in data
        assert 'token' in data['result']

        assert data['status']
        token_str = data['result']['token']
        assert is_token_valid(token_str)

        token = Token.objects(token=token_str).first()
        token.delete()
        assert not Token.objects(token=token_str).first()

    def test_users_expire_token_success(self):
        response = self.client.post(url_for('views.users_expire'), data=dict(token=token1uuid))
        assert response.status_code == 200

        data = json.loads(response.data)
        print data['status']
        assert 'status' in data
        assert data['status']

    def test_users_expire_expired_token(self):
        response = self.client.post(url_for('views.users_expire'), data=dict(token=expired_token))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert not data['status']


if __name__ == '__main__':
    pytest.main()
