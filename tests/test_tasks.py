import json


def test_create_task(client):
    response = client.post('/tasks', 
                          json={'title': 'Test Task', 'description': 'Test Description'},
                          content_type='application/json')
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'
    assert 'id' in data


def test_create_task_missing_title(client):
    response = client.post('/tasks', 
                          json={'description': 'Test Description'},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_get_tasks(client):
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})
    
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2


def test_get_task(client):
    create_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(create_response.data)['id']
    
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Test Task'


def test_get_task_not_found(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404


def test_update_task(client):
    create_response = client.post('/tasks', json={'title': 'Original Title'})
    task_id = json.loads(create_response.data)['id']
    
    response = client.put(f'/tasks/{task_id}', 
                         json={'title': 'Updated Title'},
                         content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Updated Title'


def test_update_task_not_found(client):
    response = client.put('/tasks/999', json={'title': 'Updated Title'})
    assert response.status_code == 404


def test_delete_task(client):
    create_response = client.post('/tasks', json={'title': 'Test Task'})
    task_id = json.loads(create_response.data)['id']
    
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204
    
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete('/tasks/999')
    assert response.status_code == 404
