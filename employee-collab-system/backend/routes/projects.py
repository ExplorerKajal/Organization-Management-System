from flask import Blueprint, request, jsonify
from extensions import db
from models import Project
from flask_jwt_extended import jwt_required, get_jwt_identity

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

# Create a new project
@projects_bp.route('/', methods=['POST'])
@jwt_required()
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description', '')

    if not name:
        return jsonify({"message": "Project name is required"}), 400

    new_project = Project(name=name, description=description)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Project created successfully", "project": {"id": new_project.id, "name": new_project.name}}), 201

# Get all projects
@projects_bp.route('/', methods=['GET'])
@jwt_required()
def get_projects():
    projects = Project.query.all()
    result = [{"id": p.id, "name": p.name, "description": p.description} for p in projects]
    return jsonify(result), 200

# Update a project
@projects_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    db.session.commit()
    return jsonify({"message": "Project updated successfully"}), 200

# Delete a project
@projects_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"}), 200
