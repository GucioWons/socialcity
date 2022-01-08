from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='post_photos', null=True)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    #user.post_likes.all()
