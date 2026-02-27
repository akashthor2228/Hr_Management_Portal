from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('admin','Admin'),
        ('hr','Hr'),
        ('student','Student'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.username