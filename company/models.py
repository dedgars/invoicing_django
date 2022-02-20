from django.db import models

class Company(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    registration = models.CharField(max_length=20, blank=True)
    vat = models.CharField(max_length=20, blank=True)
    bank = models.CharField(max_length=100, blank=True)
    swift = models.CharField(max_length=100, blank=True)
    account = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.CharField(max_length=100, blank=True)
    notes = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f'{self.name}'