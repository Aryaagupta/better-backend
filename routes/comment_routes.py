from flask import Blueprint, request, jsonify
from models import db, Task, Comment
from datetime import datetime, UTC

comment_bp = Blueprint('comments', __name__)


@comment_bp.route('/tasks/<int:task_id>/comments', methods=['POST'])
def create_comment(task_id):
    # check if task exists
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400
    
    if not data['content'].strip():
        return jsonify({'error': 'Content cannot be empty'}), 400
    
    comment = Comment(
        task_id=task_id,
        content=data['content']
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 201


@comment_bp.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([comment.to_dict() for comment in comments]), 200


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': 'Content is required'}), 400
    
    if not data['content'].strip():
        return jsonify({'error': 'Content cannot be empty'}), 400
    
    # update comment content and timestamp
    comment.content = data['content']
    comment.updated_at = datetime.now(UTC)
    db.session.commit()
    
    return jsonify(comment.to_dict()), 200


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    db.session.delete(comment)
    db.session.commit()
    
    return '', 204
