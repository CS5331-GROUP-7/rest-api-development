import pytest
import json
import hashlib
import datetime
from flask import url_for
from src.service.app import User, Token, SALT, Diary, Counter

user1 = "user1"
user1pw = "password1"
user1name = "user1"
user1age = "1"

user2 = "user2"
user2pw = "password2"
user2name = "user2"
user2age = "2"

diary_time = datetime.datetime.now().isoformat()
diary_public_id = 111
diary_public_title = 'Public title'
diary_public_text = 'Public text'

diary_private_id = 222
diary_private_title = 'Private title'
diary_private_text = 'Private text'

token1uuid = "9cbf0381-38f0-46e3-8709-831e7ecbdd2e"
token2uuid = "a3a95081-a9af-4122-91cf-1804dbe8ad01"
expired_token = "2f1830bb-46d9-4df4-b456-93d3c15c9198"
localhost = '127.0.0.1'


def add_user(username, name, age, pw):
    hash_password = hashlib.sha512(pw + SALT + username).hexdigest()
    User(username=username, hashed_password=hash_password, fullname=name, age=age).save()
    user = User.objects(username=username).first()
    userid_str = str(user.pk)
    user.update(userid=userid_str)
    return userid_str


def add_token(token_str, data, expired=False):
    token = Token(token=token_str, data=json.dumps(data), isexpired=expired)
    token.save()


def add_diary(diary_id, title, username, published_time, public, text):
    Diary(id=diary_id, title=title, username=username, published_time=published_time, public=public, text=text).save()


def delete_user(username):
    user = User.objects(username=username).first()
    user.delete()


def delete_token(token_str):
    token = Token.objects(token=token_str).first()
    if token:
        token.delete()


def delete_diary(diary_id):
    diary = Diary.objects(id=diary_id).first()
    if diary:
        diary.delete()


@pytest.mark.usefixtures('client_class')
class TestDiaryNonEmpty(object):
    @classmethod
    def setup_class(cls):
        user1id = add_user(user1, user1name, user1age, user1pw)
        data = {'pk': user1id, 'ip': localhost}
        add_token(token1uuid, data)
        add_token(expired_token, data, True)

        user2id = add_user(user2, user2name, user2age, user2pw)
        data = {'pk': user2id, 'ip': localhost}
        add_token(token2uuid, data)

        add_diary(diary_public_id, diary_public_title, user1, diary_time, True, diary_public_text)
        add_diary(diary_private_id, diary_private_title, user1, diary_time, False, diary_private_text)

    @classmethod
    def teardown_class(cls):
        delete_user(user1)
        delete_user(user2)

        delete_token(token1uuid)
        delete_token(expired_token)
        delete_token(token2uuid)

        delete_diary(diary_public_id)
        delete_diary(diary_private_id)

    def test_diary_get(self):
        response = self.client.get(url_for('diary'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'result' in data
        assert 'status' in data

        assert data['status']
        assert len(data['result']) == 1

        diary_data = json.loads(data['result'][0])
        assert diary_data['id'] == int(diary_public_id)
        assert diary_data['title'] == diary_public_title
        assert diary_data['author'] == user1
        assert diary_data['publish_date'] == diary_time
        assert diary_data['public']
        assert diary_data['text'] == diary_public_text

    def test_diary_post_owner(self):
        response = self.client.post(url_for('diary'),
                                    data=dict(token=token1uuid),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'result' in data
        assert 'status' in data

        assert data['status']
        assert len(data['result']) == 2

        diary_data = json.loads(data['result'][1])
        assert diary_data['id'] == int(diary_private_id)
        assert diary_data['title'] == diary_private_title
        assert diary_data['author'] == user1
        assert diary_data['publish_date'] == diary_time
        assert not diary_data['public']
        assert diary_data['text'] == diary_private_text

    def test_diary_post_not_owner(self):
        response = self.client.post(url_for('diary'),
                                    data=dict(token=token2uuid),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'result' in data
        assert 'status' in data

        assert data['status']
        assert len(data['result']) == 0

    def test_diary_create(self):
        response = self.client.post(url_for('diary_creation'),
                                    data=dict(token=token2uuid),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'id' in data
        assert 'status' in data

        assert data['status']
        assert data['id'] == 1

        count = Counter.objects()[0]
        count.update(count=0)
        delete_diary(data['id'])

    def test_diary_delete_not_owner(self):
        response = self.client.post(url_for('diary_delete'),
                                    data=dict(token=token2uuid, id=diary_private_id),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert not data['status']

    def test_diary_delete_owner(self):
        add_diary(999, "test_diary_delete", user2, diary_time, True, "user2 owner")
        response = self.client.post(url_for('diary_delete'),
                                    data=dict(token=token2uuid, id=999),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert data['status']

        diary = Diary.objects(id=999).first()
        assert not diary

    def test_diary_permission_not_owner(self):
        response = self.client.post(url_for('diary_permission'),
                                    data=dict(token=token2uuid, id=diary_private_id, public=True),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert not data['status']

        diary = Diary.objects(id=diary_private_id).first()
        assert not diary.public

    def test_diary_permission_owner_private_to_public(self):
        response = self.client.post(url_for('diary_permission'),
                                    data=dict(token=token1uuid, id=diary_private_id, public=True),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert data['status']

        diary = Diary.objects(id=diary_private_id).first()
        assert diary.public

    def test_diary_permission_owner_public_to_private(self):
        response = self.client.post(url_for('diary_permission'),
                                    data=dict(token=token1uuid, id=diary_public_id, public=False),
                                    environ_base={'REMOTE_ADDR': localhost})
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'status' in data
        assert data['status']

        diary = Diary.objects(id=diary_public_id).first()
        assert not diary.public


if __name__ == '__main__':
    pytest.main()