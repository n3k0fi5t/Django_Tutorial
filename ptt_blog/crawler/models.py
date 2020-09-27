from django.db import models

from enum import IntEnum

class TaskStatus(IntEnum):
    QUEUING = 0
    RUNNING = 1
    FINISH = 2
    ERROR = 3


TASK_STATUS_CHOICES = (
    (TaskStatus.QUEUING, 'In Queue'),
    (TaskStatus.RUNNING, 'Running'),
    (TaskStatus.FINISH, 'Finished'),
    (TaskStatus.ERROR, 'Error')
)

# Create your models here.
class CrawlTask(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    submit_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=TASK_STATUS_CHOICES, default=0)

    class Meta:
        ordering = ['-update_time', '-submit_time']