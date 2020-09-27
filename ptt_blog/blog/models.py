from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordered = ['-date', ]


class Push(models.Model):
    pusher = models.CharField(max_length=50)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostImage(models.Model):
    url = models.TextField(null=False)
    post = models.ManyToManyField(Post)
