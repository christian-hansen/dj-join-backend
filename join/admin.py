from django.contrib import admin

# Register your models here.
from .models import TaskItem, ContactItem, SubTaskItem

admin.site.register(TaskItem)
admin.site.register(SubTaskItem)
admin.site.register(ContactItem)