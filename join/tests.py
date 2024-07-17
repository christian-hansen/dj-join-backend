from django.test import TestCase, Client
from django.contrib.auth.models import User


# Create your tests here.
class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password='test_password', email='test@example.com')

    def test_login_success(self):
        # Test successful login
        response = self.client.post('/api/v1/login/', {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('email' in response.data)
        
    def test_login_failure(self):
        # Test failed login with incorrect password
        response = self.client.post('/api/v1/login/', {'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 400)  # Expecting 400 Bad Request for failed login

        # Test failed login with non-existent user
        response = self.client.post('/api/v1/login/', {'username': 'nonexistent_user', 'password': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_credentials(self):
        # Test login with missing credentials
        response = self.client.post('/api/v1/login/', {'username': 'test_user'})
        self.assertEqual(response.status_code, 400)  # Expecting 400 Bad Request for missing password