from django.contrib import admin

# Register your models here.
from .models import TaskItem

admin.site.register(TaskItem)