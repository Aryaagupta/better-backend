from flask import Blueprint, request, jsonify
from models import db, Task

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        status=data.get('status', 'pending')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks]), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']
    
    db.session.commit()
    return jsonify(task.to_dict()), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    return '', 204
