import unittest
from app import create_app, db
from models.user import User
from models.chat import Chat, Message

class DashboardTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        
        # Create test user
        self.user = User(username='testuser', email='test@example.com', password='password123')
        db.session.add(self.user)
        db.session.commit()
        
        # Log in the test user
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember_me': False
        })
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_dashboard_access(self):
        """Test accessing the dashboard."""
        response = self.client.get('/dashboard/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Your Chats', response.data)
    
    def test_dashboard_with_chats(self):
        """Test dashboard display with existing chats."""
        # Create some chats for the user
        chat1 = Chat(user_id=self.user.id, title="First Chat")
        chat2 = Chat(user_id=self.user.id, title="Second Chat")
        db.session.add(chat1)
        db.session.add(chat2)
        db.session.commit()
        
        # Add messages to the chats
        message1 = Message(content="Hello", is_user=True, chat_id=chat1.id)
        message2 = Message(content="Hi there", is_user=False, chat_id=chat1.id)
        db.session.add(message1)
        db.session.add(message2)
        db.session.commit()
        
        # Access the dashboard
        response = self.client.get('/dashboard/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that chat titles appear in the response
        self.assertIn(b'First Chat', response.data)
        self.assertIn(b'Second Chat', response.data)
        
        # Check that statistics are correct
        self.assertIn(b'Total Chats</div>', response.data)
        self.assertIn(b'<div class="stats-value">2</div>', response.data)  # 2 chats
        self.assertIn(b'Total Messages</div>', response.data)
        self.assertIn(b'<div class="stats-value">2</div>', response.data)  # 2 messages
    
    def test_dashboard_sorting(self):
        """Test dashboard sorting options."""
        # Create some chats with different timestamps
        import time
        from datetime import datetime, timedelta
        
        # Create first chat (oldest)
        chat1 = Chat(user_id=self.user.id, title="Z Chat")
        chat1.created_at = datetime.utcnow() - timedelta(days=2)
        chat1.updated_at = chat1.created_at
        db.session.add(chat1)
        db.session.commit()
        
        # Create second chat (newest)
        time.sleep(0.1)  # Ensure different timestamps
        chat2 = Chat(user_id=self.user.id, title="A Chat")
        db.session.add(chat2)
        db.session.commit()
        
        # Test newest first (default)
        response = self.client.get('/dashboard/', follow_redirects=True)
        content = response.data.decode('utf-8')
        # Check order of chats (newest should be first)
        self.assertTrue(content.find('A Chat') < content.find('Z Chat'))
        
        # Test oldest first
        response = self.client.get('/dashboard/?sort=oldest', follow_redirects=True)
        content = response.data.decode('utf-8')
        # Check order of chats (oldest should be first)
        self.assertTrue(content.find('Z Chat') < content.find('A Chat'))
        
        # Test by title
        response = self.client.get('/dashboard/?sort=title', follow_redirects=True)
        content = response.data.decode('utf-8')
        # Check order of chats (alphabetical by title)
        self.assertTrue(content.find('A Chat') < content.find('Z Chat'))
    
    def test_dashboard_empty(self):
        """Test dashboard display with no chats."""
        # Access the dashboard without creating any chats
        response = self.client.get('/dashboard/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check for empty state message
        self.assertIn(b'No Chats Yet', response.data)
        self.assertIn(b'Start a new conversation', response.data)
    
    def test_dashboard_requires_login(self):
        """Test that dashboard access requires authentication."""
        # Logout the current user
        self.client.get('/auth/logout', follow_redirects=True)
        
        # Try to access dashboard
        response = self.client.get('/dashboard/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Should be redirected to login page
        self.assertIn(b'Login', response.data)
        self.assertNotIn(b'Your Chats', response.data)

if __name__ == '__main__':
    unittest.main()
