from flask import Blueprint, request, jsonify
from extensions import db
from models import Department, User
from flask_jwt_extended import jwt_required, get_jwt

departments_bp = Blueprint('departments', __name__, url_prefix='/departments')

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') != 'Admin':
            return jsonify({"message": "Admin priority required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

def manager_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('role') not in ['Admin', 'Manager']:
            return jsonify({"message": "Manager or Admin priority required"}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@departments_bp.route('', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    return jsonify([d.to_dict() for d in departments]), 200

@departments_bp.route('', methods=['POST'])
@manager_required
def create_department():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    manager_id = data.get('manager_id')

    if not name:
        return jsonify({"message": "Department name is required"}), 400

    if Department.query.filter_by(name=name).first():
        return jsonify({"message": "Department already exists"}), 400

    new_dept = Department(name=name, description=description, manager_id=manager_id)
    db.session.add(new_dept)
    db.session.commit()

    return jsonify(new_dept.to_dict()), 201

@departments_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_department(id):
    dept = Department.query.get_or_404(id)
    return jsonify(dept.to_dict()), 200

@departments_bp.route('/<int:id>', methods=['PUT'])
@manager_required
def update_department(id):
    dept = Department.query.get_or_404(id)
    data = request.get_json()

    dept.name = data.get('name', dept.name)
    dept.description = data.get('description', dept.description)
    dept.manager_id = data.get('manager_id', dept.manager_id)

    db.session.commit()
    return jsonify(dept.to_dict()), 200

@departments_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_department(id):
    dept = Department.query.get_or_404(id)
    db.session.delete(dept)
    db.session.commit()
    return jsonify({"message": "Department deleted successfully"}), 200
