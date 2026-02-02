from app import create_app
from models import User
from extensions import db

app = create_app()
with app.app_context():
    print(f"DB URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    try:
        users = User.query.all()
        print(f"Users found: {len(users)}")
    except Exception as e:
        print(f"Error: {e}")
