from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

   
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
     #might not always work, if the ordering is not the same
    assert posts_list[0].Post.id == test_posts[0].id 

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 401


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts')
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get('detail') == 'Not authenticated'

def test_post_that_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404
    assert res.json().get('detail') == 'post with id: 88888 not found'

def test_get_one_post(authorized_client, test_posts):    
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    
 
@pytest.mark.parametrize('title, content, published', [
    ('Awesome New Pizza', 'Pepparoni iko na macoroni', True),
    ('Githeri ya Upank', 'Githeri na cheese', False),
    ('Mrenda ugali', 'Chakula inatelza', True),
])   
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post('/posts/', json={'title': title, 'content': content, 'published': published})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    
def test_create_post_with_default_published(authorized_client, test_user, test_posts):
    res = authorized_client.post('/posts/', json={'title': 'title', 'content': 'content'})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == 'title'
    assert created_post.content == 'content'
    assert created_post.published == True
    
def test_unauthorized_user_create_post(client, test_posts):
    res = client.post('/posts/', json={'title': 'title', 'content': 'content'})
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204
    
def test_delete_non_existing_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/88888")
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_posts, test_user2):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    
    
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title' : 'one',
        'content': 'two',
        'published': False
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200
    
def test_unauthorized_update_post(client, test_user, test_posts):
    data = {
        'title' : 'one',
        'content': 'two',
        'published': False
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401
    
def test_update_other_user_post(client, test_user, test_posts):
    data = {
        'title' : 'one',
        'content': 'two',
        'published': False
    }
    res = client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401
    

def test_update_non_existing_post(authorized_client, test_user, test_posts):
    data = {
        'title' : 'one',
        'content': 'two',
        'published': False
    }
    res = authorized_client.put(f"/posts/88888", json=data)
    assert res.status_code == 404