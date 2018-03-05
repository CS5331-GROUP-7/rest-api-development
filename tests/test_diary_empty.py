import pytest
import json
from flask import url_for
from src.service.models import Diary
from utils import send_post_data

@pytest.mark.usefixtures('client_class')
class TestDiaryEmpty(object):
    def test_diary_get_empty(self):
        diary = Diary.objects(id=999).first()
        if diary:
            diary.delete()
        response = self.client.get(url_for('views.diary'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'result' in data
        assert 'status' in data

        assert data['status']
        assert len(data['result']) == 0

    def test_diary_post_no_token(self):
        response = send_post_data(self.client,url_for('views.diary'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_post_invalid_token(self):
        response = send_post_data(self.client,url_for('views.diary'), data=dict(token="e7326198-7055-4559-8d2b-b4568855211e"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_create_no_token(self):
        response = send_post_data(self.client,url_for('views.diary_creation'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_create_invalid_token(self):
        response = send_post_data(self.client,url_for('views.diary_creation'), data=dict(token="e7326198-7055-4559-8d2b-b4568855211e"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_delete_no_token(self):
        response = send_post_data(self.client,url_for('views.diary_delete'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_delete_invalid_token(self):
        response = send_post_data(self.client,url_for('views.diary_delete'), data=dict(token="e7326198-7055-4559-8d2b-b4568855211e"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_permission_no_token(self):
        response = send_post_data(self.client,url_for('views.diary_permission'))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']

    def test_diary_permission_invalid_token(self):
        response = send_post_data(self.client,url_for('views.diary_permission'), data=dict(token="e7326198-7055-4559-8d2b-b4568855211e"))
        assert response.status_code == 200

        data = json.loads(response.data)
        assert 'error' in data
        assert 'status' in data

        assert not data['status']
        assert 'Invalid authentication token' in data['error']


if __name__ == '__main__':
    pytest.main()
