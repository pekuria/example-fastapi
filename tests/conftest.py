from fastapi.testclient import TestClient
import pytest
from app import models

from app.config import settings
from app.main import app
from app.database import get_db, Base
from app.oauth2 import create_access_token

from .database import TestingSessionLocal, Base, engine


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': 'imanimu4@gmail.com', 'password': 'lunagal'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {'email': 'imanimu5@gmail.com', 'password': 'lunagal'}
    res = client.post('/users/', json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            'title': 'Siku Njema',
            'content': 'kongowea alikua toast',
            'owner_id': test_user['id']
        },
        {
            'title': 'Things Fall Apart',
            'content': 'Okwongo, who killed the banana tree',
            'owner_id': test_user['id']
        },
        {
            'title': 'Amezidi',
            'content': 'Mambo imekua too much',
            'owner_id': test_user['id']
        },
        {
            'title': 'River And The Source',
            'content': 'Aoko mambo baaad',
            'owner_id': test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, posts_data)

    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    return posts
