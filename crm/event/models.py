from django.db import models
from django.conf import settings


class Customer(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile = models.IntegerField()
    phone = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='customer')
    saler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')


class Company(models.Model):

    name = models.CharField(max_length=255)


class Contract(models.Model):
    CHOICES_STATUS = (
        ("SIGNE", "Signé"),
        ("EN COURS", "En cours"),
    )

    type = models.CharField(max_length=15, choices=CHOICES_STATUS, default="MANAGEMENT")
    amount = models.FloatField()
    payement_due = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField()
    customer = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='contract')
    saler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contract')