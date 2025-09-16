import uuid

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
    is_active = models.BooleanField(
        verbose_name="активированный аккаунт", 
        default=False
    )
    activation_code = models.UUIDField(
        verbose_name="код активации", 
        unique=True, 
        default=uuid.uuid4
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("id",)
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return f"{self.pk} -> {self.email}"