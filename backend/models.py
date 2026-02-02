from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='Employee') # 'Admin', 'Manager', 'Employee'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Key to Department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    
    # Relationships
    tasks = db.relationship('Task', backref='assignee', lazy=True)
    # Note: 'department' relationship is defined in Department model using backref

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "department_id": self.department_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(200))
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    employees = db.relationship('User', foreign_keys=[User.department_id], backref='department', lazy=True)
    manager = db.relationship('User', foreign_keys=[manager_id], remote_side=[User.id], backref='managed_department')
    projects = db.relationship('Project', backref='department', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "manager_id": self.manager_id,
            "manager_name": self.manager.username if self.manager else None,
            "employee_count": len(self.employees) if self.employees else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Not Started') # 'Not Started', 'In Progress', 'Completed', 'On Hold'
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "status": self.status,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending') # 'Pending', 'In Progress', 'Completed'
    priority = db.Column(db.String(20), default='Medium') # 'Low', 'Medium', 'High'
    deadline = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "project_id": self.project_id,
            "project_name": self.project.name if self.project else None,
            "assigned_to": self.assigned_to,
            "assigned_user_name": self.assignee.username if self.assignee else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
