from django.contrib import auth
from django.db import models

# Create your models here.
class User(auth.models.AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_name = models.TextField(null=True)

    class Meta:
        db_table = "user_profile"