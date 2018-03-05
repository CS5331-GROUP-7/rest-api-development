import pytest
import json
from flask import url_for


def test_meta_heartbeat(client):
    page = client.get(url_for('meta_heartbeat'))
    assert page.status_code == 200

    data = json.loads(page.data)
    assert 'status' in data
    assert data['status']


def test_meta_members(client):
    page = client.get(url_for('meta_members'))
    assert page.status_code == 200

    data = json.loads(page.data)
    assert 'status' in data
    assert 'result' in data

    assert data['status']
    assert data['result'] == ['Zawlin', 'Xue Si', 'Shi Qing', 'Chen Hui']


if __name__ == '__main__':
    pytest.main()
