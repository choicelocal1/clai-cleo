import os
from app import create_app, db
from models.user import User
from models.chat import Chat, Message
from flask_migrate import upgrade

app = create_app(os.getenv('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """Make certain objects automatically available in the shell context."""
    return {
        'db': db,
        'User': User,
        'Chat': Chat,
        'Message': Message
    }

@app.cli.command("init-db")
def init_db():
    """Initialize the database with tables."""
    db.create_all()
    print("Database initialized with all tables.")

@app.cli.command("create-admin")
def create_admin():
    """Create an admin user for testing."""
    admin = User.query.filter_by(email='admin@example.com').first()
    if admin is None:
        admin = User(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")

if __name__ == '__main__':
    app.run(debug=True)
