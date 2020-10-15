from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class PostManager(models.Manager):
    def all(self, *args, **kargs):
        return super(PostManager, self).all()

def upload_location(instance, filename):
    return "{0}/{1}".format(instance.id, filename)

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    # for draft
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    slug = models.SlugField(unique=True)

    image = models.ImageField(
        upload_to=upload_location,
        null=True,
        blank=True,
        width_field='width_field',
        height_field='height_field'
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id" : self.id,})

    