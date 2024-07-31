from rest_framework import serializers
from join.models import TaskItem


class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskItem
        fields = "__all__"
