from django.shortcuts import render, redirect
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views import View
from join.models import TaskItem, ContactItem, SubTaskItem
from join.serializers import TaskItemSerializer, UserItemSerializer, ContactItemSerializer, SubTaskItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class LoginView(ObtainAuthToken):
    """ View to login a user """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class RegisterView(APIView):
    """ View to register a user including error responses. """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the user
            user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListTasks(APIView):
    """ View to load all tasks from the database """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = TaskItem.objects.all() # option to show all tasks for all users
        # tasks = TaskItem.objects.filter(author=request.user) # option to show only the user tasks for the current user
        serializer = TaskItemSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()  # Make a copy of the request data
        data['author'] = request.user.id # Add the author using the current user

        serializer = TaskItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    """ View to load a single tasks by its ID from the database. """
    
    def get(self, request, pk):
        task = TaskItem.objects.filter(id=pk)
        serializer = TaskItemSerializer(task, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            task = TaskItem.objects.get(pk=pk)
        except TaskItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            todo = TaskItem.objects.get(pk=pk)
        except TaskItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskItemSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListSubTasks(APIView):
    """ View to load all subtasks from the database """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        subtasks = SubTaskItem.objects.all()
        serializer = SubTaskItemSerializer(subtasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
       # Extract the task and title from the request data
        task_id = request.data.get('task')
        title = request.data.get('title')
        
        # Ensure the task ID is provided
        if not task_id:
            return Response({'task': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'title': title,
            'task': task_id
        }


        serializer = SubTaskItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailView(APIView):
    """ View to load a single subtasks by its ID from the database. """
    
    def get(self, request, pk):
        subtask = SubTaskItem.objects.filter(id=pk)
        serializer = SubTaskItemSerializer(subtask, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            subtask = SubTaskItem.objects.get(pk=pk)
        except SubTaskItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            subtask = SubTaskItem.objects.get(pk=pk)
        except SubTaskItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskItemSerializer(subtask, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskSubtasksView(APIView):
    """View to list all subtasks for a specific task."""

    def get(self, request, task_id, format=None):
        subtasks = SubTaskItem.objects.filter(task_id=task_id)
        
        if not subtasks.exists():
            return Response({'detail': 'No subtasks found for this task.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SubTaskItemSerializer(subtasks, many=True)
        return Response(serializer.data)

class ListUsers(APIView):
    """ View to load all users from the database. """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        users = User.objects.all() 
        serializer = UserItemSerializer(users, many=True)
        return Response(serializer.data)
    
class CurrentUserView(APIView):
    """ View to load the current logged in user from the database. """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id
        })

class ListContacts(APIView):
    """ View to load all contacts from the database """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        contacts = ContactItem.objects.all()
        serializer = ContactItemSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
        }


        serializer = ContactItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactDetailView(APIView):
    """ View to load a single contact by its ID from the database. """
    
    def get(self, request, pk):
        contact = ContactItem.objects.filter(id=pk)
        serializer = ContactItemSerializer(contact, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            contact = ContactItem.objects.get(pk=pk)
        except TaskItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            contact = ContactItem.objects.get(pk=pk)
        except ContactItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ContactItemSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)