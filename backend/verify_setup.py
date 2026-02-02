from app import create_app
from extensions import db
from models import User
import sys

try:
    print("Initializing app...")
    app = create_app()
    with app.app_context():
        # Check extensions
        if not app.extensions.get('sqlalchemy'):
            print("Error: SQLAlchemy not initialized")
            sys.exit(1)
            
        # Check models
        # Ensure User model is known to SQLAlchemy
        if 'users' not in db.metadata.tables:
             print("Error: User model not found in metadata. Tables found:", db.metadata.tables.keys())
             sys.exit(1)
        
        print("Verification Successful: App created, Database initialized, User model found.")
except Exception as e:
    print(f"Verification Failed: {e}")
    sys.exit(1)
