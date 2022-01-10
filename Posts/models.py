from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='post_photos', null=True)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    #user.post_likes.all()

    def get_like_url(self):
        return reverse('accounts:like-view', kwargs={'my_id': self.id})
    def get_dislike_url(self):
        return reverse('accounts:dislike-view', kwargs={'my_id': self.id})