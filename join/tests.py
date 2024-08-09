from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token  # Import Token model
from django.contrib.auth.models import User
from join.models import TaskItem
from join.serializers import TaskItemSerializer
from rest_framework import status


class LoginTest(TestCase):
    # Tests for login
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')

    def test_login_success(self):
        # Test successful login
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('email' in response.data)

    def test_login_failure(self):
        # Test failed login with incorrect password
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user', 'password': 'wrong_password'})
        # Expecting 400 Bad Request for failed login
        self.assertEqual(response.status_code, 400)

        # Test failed login with non-existent user
        response = self.client.post(
            '/api/v1/login/', {'username': 'nonexistent_user', 'password': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_credentials(self):
        # Test login with missing credentials
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user'})
        # Expecting 400 Bad Request for missing password
        self.assertEqual(response.status_code, 400)

    def test_logout_view(self):
        response = self.client.get('/logout')
        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)


class RegisterViewTest(TestCase):
    # Tests for registration
    
    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        # Test successful registration
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com', 'first_name' : 'first_name', 'last_name' : 'last_name', 'password': 'new_password'})
        self.assertEqual(response.status_code, 201)
        # Check if user is created
        self.assertEqual(User.objects.filter(username='new_user').count(), 1)

    def test_register_existing_username(self):
        # Test registration with existing username
        User.objects.create_user(
            username='existing_user', email='existing@example.com', first_name='first_name', last_name='last_name',password='existing_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'existing_user', 'email': 'another@example.com', 'first_name' : 'first_name', 'last_name' : 'last_name', 'password': 'new_password'})
        # Expecting 400 Bad Request for existing username
        self.assertEqual(response.status_code, 400)

    def test_register_existing_email(self):
        # Test registration with existing email
        User.objects.create_user(
            username='another_user', email='existing@example.com', password='another_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'existing@example.com', 'password': 'new_password'})
        # Expecting 400 Bad Request for existing email
        self.assertEqual(response.status_code, 400)

    def test_register_missing_fields(self):
        # Test registration with missing fields
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com'})
        # Expecting 400 Bad Request for missing password
        self.assertEqual(response.status_code, 400)


class TaskAPITest(TestCase):
    # Tests for task listing and creation
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

    # Test creating a task.
    def test_create_task_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        task_data = {'title': 'Test Task',
                     'description': 'Test description', 'isDone': False}

        # Send POST request with JSON data
        response = self.client.post('/api/v1/tasks/', task_data, format='json')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['description'], 'Test description')
        self.assertFalse(response.data['isDone'])

        # Validate serializer data
        # Pass response.data to serializer
        serializer = TaskItemSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())  # Validate serializer data

    # Test loading all tasks.

    def test_list_tasks(self):
        self.client.force_authenticate(user=self.user, token=self.token)

        # Send GET request to list tasks
        response = self.client.get('/api/v1/tasks/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming no tasks exist initially
        self.assertEqual(len(response.data), 0)

    # Test updating the title, description, priority, state and isDone.

    def test_update_task_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        task = TaskItem.objects.create(title='Test Task', author=self.user)
        updated_data = {'title': 'Updated Task', 'description': 'Updated description',
                        'priority': 'High', 'state': 'In Progress', 'isDone': True}

        # Send PATCH request with JSON data to update task
        response = self.client.patch(
            f'/api/v1/tasks/{task.pk}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['description'], 'Updated description')
        self.assertTrue(response.data['priority'], 'High')
        self.assertTrue(response.data['state'], 'In Progress')
        self.assertTrue(response.data['isDone'])

    # Test loading single tasks information.

    def test_task_detail(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        task = TaskItem.objects.create(title='Test Task', author=self.user)

        # Send GET request to retrieve task detail
        response = self.client.get(f'/api/v1/tasks/{task.pk}/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test Task')

    # Test deleting a single task.

    def test_delete_task(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        task = TaskItem.objects.create(title='Test Task', author=self.user)

        # Send DELETE request to delete task
        response = self.client.delete(f'/api/v1/tasks/{task.pk}/')

        # Assert response status and ensure task is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TaskItem.objects.filter(pk=task.pk).exists())
