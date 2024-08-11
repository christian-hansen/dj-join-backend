from rest_framework import serializers
from join.models import TaskItem, ContactItem
from django.contrib.auth.models import User


class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItem
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
        fields = ('id', 'first_name','last_name', 'full_name', 'email', 'is_superuser', 'is_staff')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"