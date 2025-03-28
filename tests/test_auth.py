import unittest
from flask import url_for
from app import create_app, db
from models.user import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_register_and_login(self):
        """Test user registration and login."""
        # Register a new account
        response = self.client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that the user was created
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        
        # Log out
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Log in with the new account
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Access protected page
        response = self.client.get('/dashboard/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_incorrect_login(self):
        """Test login with incorrect credentials."""
        # Register a user
        user = User(username='testuser', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        # Attempt login with incorrect password
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful', response.data)
        
        # Attempt login with non-existent email
        response = self.client.post('/auth/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login unsuccessful', response.data)
    
    def test_logout_redirect(self):
        """Test that logout redirects to homepage."""
        # Register and login a user
        user = User(username='testuser', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember_me': False
        }, follow_redirects=True)
        
        # Logout and check redirect
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)
        self.assertIn(b'Welcome to ChatBot', response.data)  # Homepage content

if __name__ == '__main__':
    unittest.main()
