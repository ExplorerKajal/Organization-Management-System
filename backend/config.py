import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    
    # Database Configuration
    # Defaults to SQLite. User can provide a different URI via DATABASE_URL environment variable.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///c:/Users/kajal/.gemini/antigravity/scratch/employee-collab-system/backend/app.db'
    print(f"DEBUG: SQLALCHEMY_DATABASE_URI = {SQLALCHEMY_DATABASE_URI}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'super-secret-key-change-this-in-production'

    # Uploads
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
