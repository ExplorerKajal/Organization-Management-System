from flask import Flask
from config import Config

# Import blueprints
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.users import users_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)

    # Initialize extensions
    from extensions import db, migrate, cors, jwt
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    jwt.init_app(app)

    # Import models to register them with SQLAlchemy
    from models import User

    @app.route('/')
    def index():
        return "Employee & Project Management API is running!"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
