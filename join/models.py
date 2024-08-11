from django.db import models
from django.conf import settings
import datetime

# Create your models here.
# Specifying the priorities
PRIORITIES = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low")
)

# Specifying the priorities
STATES = (
    ("To Do", "To Do"),
    ("In Progress", "In Progress"),
    ("Awaiting Feedback", "Awaiting Feedback"),
    ("Done", "Done")
)


class TaskItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.date.today)
    priority = models.CharField(max_length=10, choices=PRIORITIES, default='Low')
    due_date = models.DateField(default=datetime.date.today)
    state = models.CharField(max_length=20, choices=STATES, default='To Do')
    # isDone = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'({self.id}) --- {self.title}'
    
class ContactItem(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=500)
    created_at = models.DateField(default=datetime.date.today)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # priority = models.CharField(max_length=10, choices=PRIORITIES, default='Low')
    # due_date = models.DateField(default=datetime.date.today)
    # state = models.CharField(max_length=20, choices=STATES, default='To Do')
    # isDone = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'({self.id}) --- {self.first_name} {self.last_name}'