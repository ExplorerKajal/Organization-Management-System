from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Department
from flask_jwt_extended import jwt_required, get_jwt

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

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

@employees_bp.route('', methods=['GET'])
@jwt_required()
def get_employees():
    employees = User.query.all()
    return jsonify([e.to_dict() for e in employees]), 200

@employees_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    employee = User.query.get_or_404(id)
    return jsonify(employee.to_dict()), 200

@employees_bp.route('/<int:id>', methods=['PUT'])
@manager_required
def update_employee(id):
    employee = User.query.get_or_404(id)
    data = request.get_json()

    # Update role (Admin only can change roles to Admin, but let's keep it simple for now)
    if 'role' in data:
        employee.role = data['role']
    
    # Update department
    if 'department_id' in data:
        dept_id = data['department_id']
        if dept_id:
            dept = Department.query.get(dept_id)
            if not dept:
                return jsonify({"message": "Department not found"}), 404
            employee.department_id = dept_id
        else:
            employee.department_id = None

    db.session.commit()
    return jsonify(employee.to_dict()), 200

@employees_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_employee(id):
    employee = User.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Employee deleted successfully"}), 200
