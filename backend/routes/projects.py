from flask import Blueprint, request, jsonify
from extensions import db
from models import Project, Department
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

def manager_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') not in ['Admin', 'Manager']:
            return jsonify({"message": "Manager or Admin priority required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@projects_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    department_id = request.args.get('department_id', type=int)
    if department_id:
        projects = Project.query.filter_by(department_id=department_id).all()
    else:
        projects = Project.query.all()
    return jsonify([p.to_dict() for p in projects]), 200

@projects_bp.route('', methods=['POST'])
@manager_required
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    department_id = data.get('department_id')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    status = data.get('status', 'Not Started')

    if not name or not department_id:
        return jsonify({"message": "Name and department_id are required"}), 400

    dept = Department.query.get(department_id)
    if not dept:
        return jsonify({"message": "Department not found"}), 404

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None

    new_project = Project(
        name=name, 
        description=description, 
        department_id=department_id,
        start_date=start_date,
        end_date=end_date,
        status=status
    )
    db.session.add(new_project)
    db.session.commit()

    return jsonify(new_project.to_dict()), 201

@projects_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.to_dict()), 200

@projects_bp.route('/<int:id>', methods=['PUT'])
@manager_required
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()

    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    project.department_id = data.get('department_id', project.department_id)

    if 'start_date' in data:
        project.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data['start_date'] else None
    if 'end_date' in data:
        project.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data['end_date'] else None

    db.session.commit()
    return jsonify(project.to_dict()), 200

@projects_bp.route('/<int:id>', methods=['DELETE'])
@manager_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200
