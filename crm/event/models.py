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

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Company(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'

class Contract(models.Model):
    CHOICES_STATUS = (
        ("SIGNE", "Signé"),
        ("EN COURS", "En cours"),
    )

    status = models.CharField(max_length=15, choices=CHOICES_STATUS, default="En cours")
    amount = models.FloatField()
    payement_due = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='contract')
    saler = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contract')

    def __str__(self):
        return f'customer: {self.customer} saler: {self.saler}'

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
    contract = models.ForeignKey('Contract', unique=True, on_delete=models.CASCADE, related_name='event')

    def __str__(self):
        return f'support: {self.support}  event: {str(self.id)}'

class Note(models.Model):

    note = models.CharField(max_length=255)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='notes')
    customer = models.ForeignKey('Customer', null=True, on_delete=models.CASCADE, related_name='note')
    support = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='note')