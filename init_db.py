from app import create_app, db
import os

app = create_app(os.getenv('FLASK_ENV', 'development'))

with app.app_context():
    db.create_all()
    print("Database initialized successfully!")
