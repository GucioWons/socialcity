from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse, resolve

from Accounts.models import Account, Notification, Post, Request, Action, Comment
from Accounts.views import profile_page


class TestAppViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Accounts views test:")
        cls.testuser = User.objects.create_user(username='testuser', password='12345')
        cls.testuser2 = User.objects.create_user(username='testuser2', password='12345')
        cls.testaccount = Account.objects.create(user=cls.testuser)
        cls.testaccount2 = Account.objects.create(user=cls.testuser2)

    def test_profile(self):
        response = self.client.get("/profile/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/profile/1/")
        self.assertTrue(response.status_code == 200)
        response = self.client.get("/profile/5/")
        self.assertTrue(response.status_code == 404)

    def test_addfriend(self):
        response = self.client.get("/add-to-friends/2/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/add-to-friends/2/")
        self.assertTrue(Request.objects.filter(user=self.testuser).exists() == True)
        response = self.client.get("/add-to-friends/5/")
        self.assertTrue(response.status_code == 404)

    def test_removefriend(self):
        response = self.client.get("/remove-from-friends/2/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/remove-from-friends/2/")
        self.assertTrue(response.status_code == 302)
        self.testaccount.friends.add(self.testuser2)
        response = self.client.post("/remove-from-friends/2/")
        self.assertTrue(self.testaccount.friends.exists() == False)

    def test_accept_request(self):
        response = self.client.get("/accept/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/accept/1/")
        self.assertTrue(response.status_code == 404)
        notification = Notification.objects.create(user=self.testuser)
        request = Request.objects.create(user=self.testuser2, notification=notification)
        response = self.client.get("/accept/1/")
        self.assertTrue(self.testaccount.friends.exists() == True)

    def test_decline_request(self):
        response = self.client.get("/decline/2/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/decline/1/")
        self.assertTrue(response.status_code == 404)
        notification = Notification.objects.create(user=self.testuser)
        request = Request.objects.create(user=self.testuser2, notification=notification)
        response = self.client.get("/decline/1/")
        self.assertTrue(Request.objects.all().exists() == False)
        response = self.client.get("/decline/5/")
        self.assertTrue(response.status_code == 404)

    def test_like(self):
        response = self.client.get("/like/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/like/1/")
        self.assertTrue(response.status_code == 404)
        post = Post.objects.create(user=self.testuser, content='testcontent')
        response = self.client.get("/like/1/")
        self.assertTrue(post.likes.exists() == True)
        response = self.client.get("/like/1/")
        self.assertTrue(post.likes.exists() == False)
        post.dislikes.add(self.testuser)
        response = self.client.get("/like/1/")
        self.assertTrue(post.likes.exists() == True and post.dislikes.exists() == False)

    def test_dislike(self):
        response = self.client.get("/dislike/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/dislike/1/")
        self.assertTrue(response.status_code == 404)
        post = Post.objects.create(user=self.testuser, content='testcontent')
        response = self.client.get("/dislike/1/")
        self.assertTrue(post.dislikes.exists() == True)
        response = self.client.get("/dislike/1/")
        self.assertTrue(post.dislikes.exists() == False)
        post.likes.add(self.testuser)
        response = self.client.get("/dislike/1/")
        self.assertTrue(post.likes.exists() == False and post.dislikes.exists() == True)

    def test_post_view(self):
        response = self.client.get("/post/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/post/1/")
        self.assertTrue(response.status_code == 404)
        post = Post.objects.create(user=self.testuser, content='testcontent')
        response = self.client.get("/post/1/")
        response = self.client.post("/post/1/", data={'user': self.testuser, 'post': post, 'content': 'testcontent'})
        self.assertTrue(Comment.objects.all().exists() == True and Notification.objects.all().exists() == True)
        response = self.client.post("/post/1/", data={'user': self.testuser, 'post': post, 'content': 'testcontent'})
        self.assertTrue(Comment.objects.all().count() == 2 and Notification.objects.all().count() == 1)


    def test_delete_post_view(self):
        response = self.client.get("/post/delete/1/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/post/delete/1/")
        self.assertTrue(response.status_code == 404)
        post = Post.objects.create(user=self.testuser, content='testcontent')
        response = self.client.get("/post/delete/1/")
        self.assertTrue(Post.objects.all().exists() == False)
