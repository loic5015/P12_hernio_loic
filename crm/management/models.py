from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):

    CHOICES_TYPES = (
        ("MANAGEMENT", "Management"),
        ("SUPPORT", "Support"),
        ("SALER", "Saler"),
    )

    username = None
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile = models.IntegerField()
    phone = models.IntegerField()
    type = models.CharField(max_length=15, choices=CHOICES_TYPES, default="MANAGEMENT")
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []



