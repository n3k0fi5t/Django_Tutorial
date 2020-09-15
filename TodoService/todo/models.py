from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)
    is_cross_off = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_time']
        db_table = 'todo_item'