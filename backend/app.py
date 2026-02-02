from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from extensions import db, migrate, cors, jwt
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    jwt.init_app(app)

    # Import models to register them with SQLAlchemy
    from models import User

    # Blueprint registration
    from routes.auth import auth_bp
    from routes.departments import departments_bp
    from routes.employees import employees_bp
    from routes.projects import projects_bp
    from routes.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(departments_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)

    
    @app.route('/')
    def index():
        return "Employee & Project Management API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)
