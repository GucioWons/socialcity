from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=500, blank=True)
    town = models.CharField(max_length=80, blank=True)
    image = models.ImageField(blank=True)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)
