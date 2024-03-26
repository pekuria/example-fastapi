import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    
def test_vote_on_other_users_post_success(authorized_client, test_posts, test_user):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[3].id, 'dir': 1})
    assert res.status_code == 201

def test_voting_on_post_with_vote(authorized_client, test_posts, test_user, test_vote):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[3].id, 'dir': 1})
    assert res.status_code == 409
    assert res.json().get('detail') == f"user {test_user['id']} has already voted on post {test_posts[3].id}"

def test_vote_on_own_post_fail(authorized_client, test_posts, test_user):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[1].id, 'dir': 1})
    assert res.status_code == 409
    

def test_deleting_vote_on_other_users_post_success(authorized_client, test_posts, test_user, test_vote):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[3].id, 'dir': 0})
    assert res.status_code == 201
    
def test_deleting_vote_when_id_does_not_exist_success(authorized_client, test_posts, test_user):
    res = authorized_client.post('/votes/', json={'post_id': test_posts[3].id, 'dir': 0})
    assert res.status_code == 404
    
def test_deleting_vote_on_a_post_that_does_not_exist_success(authorized_client, test_posts, test_user):
    res = authorized_client.post('/votes/', json={'post_id': 800000, 'dir': 0})
    assert res.status_code == 404
    
def test_unauthorized_user_voting(client, test_posts, test_user):
    res = client.post('/votes/', json={'post_id': test_posts[0].id, 'dir': 1})
    assert res.status_code == 401