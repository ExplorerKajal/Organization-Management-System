from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from flask_jwt_extended import jwt_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

# Get all users
@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    result = [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]
    return jsonify(result), 200

# Create a new user
@users_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'Employee')

    if not username or not email or not password:
        return jsonify({"message": "Username, email, and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(username=username, email=email, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": {"id": new_user.id, "username": new_user.username}}), 201

# Update a user
@users_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

# Delete a user
@users_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
