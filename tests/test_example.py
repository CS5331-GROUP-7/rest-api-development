import pytest


def test_get_index(client):
    page = client.get('/')
    assert page.status_code == 200


if __name__ == '__main__':
    pytest.main()