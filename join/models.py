from django.db import models
from django.conf import settings
import datetime

# Create your models here.
# Specifying the priorities
PRIORITIES = (
    ("prio3", "High"),
    ("prio2", "Medium"),
    ("prio1", "Low")
)

# Specifying the priorities
STATES = (
    ("state1", "To Do"),
    ("state2", "In Progress"),
    ("state3", "Awaiting Feedback"),
    ("state4", "Done")
)


class TaskItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateField(default=datetime.date.today),
    priority = models.CharField(
        max_length=10, choices=PRIORITIES, default='prio1')
    due_date = models.DateField(default=datetime.date.today),
    state = models.CharField(max_length=10, choices=STATES, default='state1')
    isDone = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'({self.id}) --- {self.title}'
