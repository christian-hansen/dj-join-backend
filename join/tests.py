from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token  # Import Token model
from django.contrib.auth.models import User
from join.models import TaskItem, ContactItem, SubTaskItem
from join.serializers import TaskItemSerializer, ContactItemSerializer, SubTaskItemSerializer
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
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com', 'first_name': 'first_name', 'last_name': 'last_name', 'password': 'new_password'})
        self.assertEqual(response.status_code, 201)
        # Check if user is created
        self.assertEqual(User.objects.filter(username='new_user').count(), 1)

    def test_register_existing_username(self):
        # Test registration with existing username
        User.objects.create_user(
            username='existing_user', email='existing@example.com', first_name='first_name', last_name='last_name', password='existing_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'existing_user', 'email': 'another@example.com', 'first_name': 'first_name', 'last_name': 'last_name', 'password': 'new_password'})
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
                     'description': 'Test description'}

        # Send POST request with JSON data
        response = self.client.post('/api/v1/tasks/', task_data, format='json')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['description'], 'Test description')

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

    # Test updating the title, description, priority, and state.

    def test_update_task_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        task = TaskItem.objects.create(title='Test Task', author=self.user)
        updated_data = {'title': 'Updated Task', 'description': 'Updated description',
                        'priority': 'High', 'state': 'In Progress'}

        # Send PATCH request with JSON data to update task
        response = self.client.patch(
            f'/api/v1/tasks/{task.pk}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')
        self.assertEqual(response.data['description'], 'Updated description')
        self.assertTrue(response.data['priority'], 'High')
        self.assertTrue(response.data['state'], 'In Progress')

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

class SubTaskAPITest(TestCase):
    # Tests for subtask listing and creation

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')
        self.token = Token.objects.create(user=self.user)
        
     # Create a TaskItem to be used in subtask tests
        self.task = TaskItem.objects.create(
            title='Test Task',
            description='Test Task Description',
            author=self.user,
            priority='Low',
            due_date='2024-08-31',
            state='To Do'
        )

    # Test creating a subtask.
    def test_create_subtask_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        subtask_data = {
            'title': 'Test SubTask',
            'task': self.task.id  # Provide the valid task ID
        }

        # Send POST request with JSON data
        response = self.client.post('/api/v1/subtasks/', subtask_data, format='json')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test SubTask')
        self.assertEqual(response.data['task'], self.task.id)
        self.assertEqual(response.data['isDone'], False)

        # Validate serializer data
        # Pass response.data to serializer
        serializer = SubTaskItemSerializer(data=response.data)
        self.assertTrue(serializer.is_valid())  # Validate serializer data
    
    # Test loading all tasks. 

    def test_list_subtasks(self):
        self.client.force_authenticate(user=self.user, token=self.token)

        # Send GET request to list subtasks
        response = self.client.get('/api/v1/subtasks/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming no subtasks exist initially
        self.assertEqual(len(response.data), 0)
    
    # TODO Test load all subtasks for one task

   
    # # Test updating the title and isDone.

    def test_update_subtask_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        subtask = SubTaskItem.objects.create(title='Test SubTask', task=self.task)
        updated_data = {'title': 'Updated SubTask', 'isDone' : True}

        # Send PATCH request with JSON data to update task
        response = self.client.patch(
            f'/api/v1/subtasks/{subtask.pk}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated SubTask')
        self.assertEqual(response.data['isDone'], True)

    # # Test loading single tasks information.

    def test_subtask_detail(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        subtask = SubTaskItem.objects.create(title='Test SubTask', task=self.task)

        # Send GET request to retrieve task detail
        response = self.client.get(f'/api/v1/subtasks/{subtask.pk}/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Test SubTask')

    # Test deleting a single task.

    def test_delete_subtask(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        subtask = SubTaskItem.objects.create(title='Test SubTask To Delete', task=self.task)

        # Send DELETE request to delete task
        response = self.client.delete(f'/api/v1/subtasks/{subtask.pk}/')

        # Assert response status and ensure task is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(SubTaskItem.objects.filter(pk=subtask.pk).exists())
        
    # Test additing a subtask to a non-exisiting task.
    def test_create_subtask_invalid_task(self):
        """Test creating a subtask with an invalid task ID"""
        self.client.force_authenticate(user=self.user, token=self.token)
        subtask_data = {
            'title': 'Test SubTask',
            'task': 9999  # Provide a non-existent task ID
        }

        # Send POST request with JSON data
        response = self.client.post('/api/v1/subtasks/', subtask_data, format='json')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('task', response.data)  # Ensure the 'task' field is in the response
        self.assertEqual(response.data['task'][0], 'Invalid pk "9999" - object does not exist.')

class ContactAPITest(TestCase):
    # Tests for contacts listing and creation

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')
        self.token = Token.objects.create(user=self.user)

    # Test loading all contacts.

    def test_list_contacts(self):
        self.client.force_authenticate(user=self.user, token=self.token)

        # Send GET request to list contacts
        response = self.client.get('/api/v1/contacts/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming no contacts exist initially
        self.assertEqual(len(response.data), 0)

    # Test updating the contacts first name and last name.

    def test_update_contact_success(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        contact = ContactItem.objects.create(
            first_name='First Name', last_name='Last Name')
        updated_data = {'first_name': 'Updated First Name',
                        'last_name': 'Updated Last Name'}

        # Send PATCH request with JSON data to update contact
        response = self.client.patch(
            f'/api/v1/contacts/{contact.pk}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated First Name')
        self.assertEqual(response.data['last_name'], 'Updated Last Name')
        self.assertTrue(response.data['full_name'],
                        'Updated First Name Updated Last Name')

    # Test loading single contacts information.

    def test_contact_detail(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        contact = ContactItem.objects.create(
            first_name='First Name', last_name='Last Name')
        # Send GET request to retrieve contact detail
        response = self.client.get(f'/api/v1/contacts/{contact.pk}/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'First Name')
        self.assertEqual(response.data[0]['last_name'], 'Last Name')

    # Test deleting a single contact.

    def test_delete_contact(self):
        self.client.force_authenticate(user=self.user, token=self.token)
        contact = ContactItem.objects.create(
            first_name='First Name', last_name='Last Name')

        # Send DELETE request to delete contact
        response = self.client.delete(f'/api/v1/contacts/{contact.pk}/')

        # Assert response status and ensure contact is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ContactItem.objects.filter(pk=contact.pk).exists())
