import pytest
import json
from flask import Flask, url_for
from src.service.app import ENDPOINT_LIST


def test_get_index(client):
    page = client.get(url_for('views.index'))  # can use the endpoint(method) name here
    assert page.status_code == 200  # response code

    data = json.loads(page.data)  # response data
    assert 'result' in data
    assert 'status' in data

    assert data['status']
    assert data['result'] == ENDPOINT_LIST


if __name__ == '__main__':
    pytest.main()
