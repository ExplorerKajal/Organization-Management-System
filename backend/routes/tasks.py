from flask import Blueprint, request, jsonify
from extensions import db
from models import Task, Project, User
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def manager_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') not in ['Admin', 'Manager']:
            return jsonify({"message": "Manager or Admin priority required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    project_id = request.args.get('project_id', type=int)
    assigned_to = request.args.get('assigned_to', type=int)
    
    query = Task.query
    if project_id:
        query = query.filter_by(project_id=project_id)
    if assigned_to:
        query = query.filter_by(assigned_to=assigned_to)
        
    tasks = query.all()
    return jsonify([t.to_dict() for t in tasks]), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    project_id = data.get('project_id')
    assigned_to = data.get('assigned_to')
    priority = data.get('priority', 'Medium')
    deadline_str = data.get('deadline')

    if not title or not project_id:
        return jsonify({"message": "Title and project_id are required"}), 400

    project = Project.query.get(project_id)
    if not project:
        return jsonify({"message": "Project not found"}), 404

    deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date() if deadline_str else None

    new_task = Task(
        title=title,
        description=description,
        project_id=project_id,
        assigned_to=assigned_to,
        priority=priority,
        deadline=deadline
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201

@tasks_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.assigned_to = data.get('assigned_to', task.assigned_to)

    if 'deadline' in data:
        task.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date() if data['deadline'] else None

    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:id>', methods=['DELETE'])
@manager_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"}), 200
