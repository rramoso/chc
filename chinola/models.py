from django.db import models

# Create your models here.
class Account(models.Model):
    phone = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=55)
    state = models.CharField(max_length=55)