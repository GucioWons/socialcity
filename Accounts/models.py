from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils import timezone


class Account(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    school = models.CharField(max_length=500, null=True)
    town = models.CharField(max_length=80, null=True)
    image = models.ImageField(default='default.png', null=True)
    friends = models.ManyToManyField(User, related_name='user_friends', blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile-view', kwargs={'my_id': self.id})

    def get_add_to_friends_url(self):
        return reverse('accounts:add-to-friends', kwargs={'my_id': self.id})

    def get_remove_from_friends_url(self):
        return reverse('accounts:remove-from-friends', kwargs={'my_id': self.id})


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    photo = models.ImageField(upload_to='post_photos', null=True)
    date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    # user.post_likes.all()

    def get_like_url(self):
        return reverse('accounts:like-view', kwargs={'my_id': self.id})

    def get_dislike_url(self):
        return reverse('accounts:dislike-view', kwargs={'my_id': self.id})

    def get_delete_url(self):
        return reverse('accounts:delete-view', kwargs={'my_id': self.id})

    def get_absolute_url(self):
        return reverse('accounts:post-view', kwargs={'my_id': self.id})


class Notification(models.Model):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new = models.BooleanField(default=True)

    def get_accept_url(self):
        return reverse('accounts:accept-view', kwargs={'my_id': self.id})

    def get_decline_url(self):
        return reverse('accounts:decline-view', kwargs={'my_id': self.id})


class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, null=True, on_delete=models.CASCADE)


class Action(models.Model):
    TYPE_CHOICES = [
        ('LIKE', 'Like'),
        ('DISLIKE', 'Dislike'),
        ('COMMENT', 'Comment'),
    ]
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    notification = models.OneToOneField(Notification, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)


class Comment(models.Model):
    content = models.CharField(max_length=80)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
