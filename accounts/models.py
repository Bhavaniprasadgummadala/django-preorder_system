# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    REGULAR = 'R'
    STALL_OWNER = 'S'
    USER_TYPE_CHOICES = [
        (REGULAR, 'Regular User'),
        (STALL_OWNER, 'Stall Owner'),
    ]
    user_type = models.CharField(
        max_length=1,
        choices=USER_TYPE_CHOICES,
        default=REGULAR
    )

    def __str__(self):
        return self.username