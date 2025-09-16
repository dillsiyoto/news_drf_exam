from django.db import models
from django.contrib.auth.models import AbstractUser
from dirtyfields import DirtyFieldsMixin

class Client(DirtyFieldsMixin, AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="эл. почта", 
        max_length=30,
        unique=True
    )