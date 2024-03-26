import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == 'Hello from fastapi'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'imanimu4@gmail.com', 'password': 'lunagal'})
    new_user = schemas.UserOut(**res.json())
    assert 'imanimu4@gmail.com' == new_user.email
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM])
    id: int = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200


@pytest.mark.parametrize('username, password, status_code', [
    ('wrong_email@gmail.com', 'lunagal', 403),
    ('imanimu@gmail.com', 'wrong_password', 403),
    ('wrong_email@gmail.com', 'wrong_password', 403),
    (None, 'lunagal', 422),
    ('imanimu@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, username, password, status_code):
    res = client.post(
        '/login', data={'username': username, 'password': password}
    )

    assert res.status_code == status_code
