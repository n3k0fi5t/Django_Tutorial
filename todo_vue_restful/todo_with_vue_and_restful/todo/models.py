from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
"""
class TodoItem(models.Model):
    user = models.ForeignKey(User, blank=True ,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-create_time']
        db_table = 'todo-item'

"""


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return self.title