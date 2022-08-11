from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password=None,  **extra_fields):
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.mobile = 12345
        user.phone = 12345
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(
            email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user


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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=CHOICES_TYPES, default="MANAGEMENT")
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = CustomUserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
