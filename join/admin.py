from django.contrib import admin

# Register your models here.
from .models import TaskItem, ContactItem

admin.site.register(TaskItem)
admin.site.register(ContactItem)