from rest_framework import serializers
from join.models import TaskItem, ContactItem, SubTaskItem
from django.contrib.auth.models import User

class TaskItemSerializer(serializers.ModelSerializer):
    subtask_ids = serializers.SerializerMethodField()

    class Meta:
        model = TaskItem
        # fields = "__all__"  # Keep all existing fields
        # Optionally, specify the exact fields including the new `subtask_ids`
        fields = ['id', 'title', 'description', 'author', 'created_at', 'priority', 'due_date', 'state', 'subtask_ids']

    def get_subtask_ids(self, obj):
        # Retrieve all related subtasks and return their IDs
        return list(obj.subtasks.values_list('id', flat=True))

class SubTaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTaskItem
        fields = "__all__"

class ContactItemSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = ContactItem
        fields = "__all__"
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class UserItemSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'full_name', 'email', 'is_superuser', 'is_staff')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"