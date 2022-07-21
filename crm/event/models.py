from django.db import models
from django.conf import settings


class Customer(models.Model):

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    mobile = models.IntegerField()
    phone = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
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
    date_updated = models.DateTimeField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='contract')
    saler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contract')


class Event(models.Model):
    CHOICES_STATUS = (
        ("SIGNE", "Signé"),
        ("EN COURS", "En cours"),
        ("TERMINE", "Terminé"),
    )

    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default="SIGNE")
    attendees = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    date_event = models.DateTimeField()
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='event')
    support = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event')

class Note(models.Model):

    note = models.CharField(max_length=255)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='notes')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='note')
    support = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='note')