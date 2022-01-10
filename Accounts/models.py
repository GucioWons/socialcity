from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone

from Posts.models import Post


class Account(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=500, blank=True)
    town = models.CharField(max_length=80, blank=True)
    image = models.ImageField(blank=True)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)

    def get_absolute_url(self):
        return reverse('accounts:profile-view', kwargs={'my_id': self.id})
    def get_add_to_friends_url(self):
        return reverse('accounts:add-to-friends', kwargs={'my_id': self.id})
    def get_remove_from_friends_url(self):
        return reverse('accounts:remove-from-friends', kwargs={'my_id': self.id})

class Notification(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    new = models.BooleanField(default=True)


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Action(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type= models.CharField(max_length=50)