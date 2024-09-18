from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

class Donation(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

class Crisis(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='pending')
    is_approved = models.BooleanField(default=False)

class Inventory(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    is_relief = models.BooleanField(default=False)
