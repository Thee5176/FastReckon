from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M','Male'),
        ('F','Female'),
    ]
    
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True)
    occupancy = models.CharField(null=True, blank=True)
    city = models.CharField(max_length=50)    #TODO:get dropdown choices
    annual_income = models.PositiveIntegerField(null=True, blank=True)