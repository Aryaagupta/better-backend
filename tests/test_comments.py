import json


def test_create_comment(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    response = client.post(f'/tasks/{task_id}/comments',
                          json={'content': 'This is a test comment'},
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['content'] == 'This is a test comment'
    assert data['task_id'] == task_id
    assert 'id' in data
    assert 'created_at' in data
    assert 'updated_at' in data


def test_create_comment_task_not_found(client):
    response = client.post('/tasks/999/comments',
                          json={'content': 'Test comment'},
                          content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Task not found'


def test_create_comment_missing_content(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    response = client.post(f'/tasks/{task_id}/comments',
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Content is required'


def test_create_comment_empty_content(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    response = client.post(f'/tasks/{task_id}/comments',
                          json={'content': '   '},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Content cannot be empty'


def test_get_comments(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    client.post(f'/tasks/{task_id}/comments', json={'content': 'Comment 1'})
    client.post(f'/tasks/{task_id}/comments', json={'content': 'Comment 2'})
    client.post(f'/tasks/{task_id}/comments', json={'content': 'Comment 3'})
    
    response = client.get(f'/tasks/{task_id}/comments')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3
    assert data[0]['content'] == 'Comment 1'
    assert data[1]['content'] == 'Comment 2'
    assert data[2]['content'] == 'Comment 3'


def test_get_comments_task_not_found(client):
    response = client.get('/tasks/999/comments')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_get_comments_empty_list(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    response = client.get(f'/tasks/{task_id}/comments')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0


def test_update_comment(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    comment_response = client.post(f'/tasks/{task_id}/comments',
                                   json={'content': 'Original comment'})
    comment_id = json.loads(comment_response.data)['id']
    
    response = client.put(f'/comments/{comment_id}',
                         json={'content': 'Updated comment'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['content'] == 'Updated comment'
    assert data['id'] == comment_id


def test_update_comment_not_found(client):
    response = client.put('/comments/999',
                         json={'content': 'Updated comment'},
                         content_type='application/json')
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_update_comment_missing_content(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    comment_response = client.post(f'/tasks/{task_id}/comments',
                                   json={'content': 'Original comment'})
    comment_id = json.loads(comment_response.data)['id']
    
    response = client.put(f'/comments/{comment_id}',
                         json={},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_update_comment_empty_content(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    comment_response = client.post(f'/tasks/{task_id}/comments',
                                   json={'content': 'Original comment'})
    comment_id = json.loads(comment_response.data)['id']
    
    response = client.put(f'/comments/{comment_id}',
                         json={'content': '  '},
                         content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_delete_comment(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    comment_response = client.post(f'/tasks/{task_id}/comments',
                                   json={'content': 'Test comment'})
    comment_id = json.loads(comment_response.data)['id']
    
    response = client.delete(f'/comments/{comment_id}')
    assert response.status_code == 204
    
    get_response = client.get(f'/tasks/{task_id}/comments')
    comments = json.loads(get_response.data)
    assert len(comments) == 0


def test_delete_comment_not_found(client):
    response = client.delete('/comments/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data


def test_delete_task_cascades_comments(client):
    task_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(task_response.data)['id']
    
    client.post(f'/tasks/{task_id}/comments', json={'content': 'Comment 1'})
    client.post(f'/tasks/{task_id}/comments', json={'content': 'Comment 2'})
    
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204
