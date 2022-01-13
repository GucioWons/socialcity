import os

from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse, resolve

from Accounts.models import Account, Notification, Post, Request, Action
from Accounts.views import profile_page
from socialcity.settings import STATICFILES_DIRS


class TestAppViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Pages views test:")
        cls.testuser = User.objects.create_user(username='testuser', password='12345')
        cls.testuser2 = User.objects.create_user(username='testuser2', password='12345')
        cls.testaccount = Account.objects.create(user=cls.testuser)
        cls.testaccount2 = Account.objects.create(user=cls.testuser2)

    def test_home_page(self):
        response = self.client.get("/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/")
        self.assertTrue(response.status_code == 200)
        response = self.client.post("/", data={'user': self.testuser, 'content': 'testcontent'})
        self.assertTrue(Post.objects.all().exists() == True)
    def test_notification_page(self):
        response = self.client.get("/notifications/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/notifications/")
        self.assertTrue(response.status_code == 200)
    def test_landing_page(self):
        response = self.client.get("/landing/")
        self.assertTrue(response.status_code == 200)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/landing/")
        self.assertTrue(response.status_code == 302)
    def test_register_page(self):
        response = self.client.get("/register/")
        self.assertTrue(response.status_code == 200)
        response = self.client.post("/register/", data={'first_name': 'test', 'last_name': 'test', 'email': 'test@test.pl', 'username': 'testusername', 'password1': 'local124', 'password2': 'local124',})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated is True)
        response = self.client.get("/register/")
        self.assertTrue(response.status_code == 302)
    def test_login_page(self):
        response = self.client.get("/login/")
        self.assertTrue(response.status_code == 200)
        response = self.client.post("/login/", data={'username': 'testuser', 'password': '12345'})
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated is True)
        response = self.client.get("/login/")
        self.assertTrue(response.status_code == 302)
    def test_logout_view(self):
        self.client.force_login(user=self.testuser)
        response = self.client.get("/logout/")
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated == False)
        response = self.client.get("/logout/")
        self.assertTrue(response.status_code == 302)

    def test_search_page(self):
        response = self.client.get("/search/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/search/", data={'query': 'test'})
        self.assertTrue(response.status_code == 200)
    def test_settings_page(self):
        response = self.client.get("/settings/")
        self.assertTrue(response.status_code == 302)
        self.client.force_login(user=self.testuser)
        response = self.client.get("/settings/")
        self.assertTrue(response.status_code == 200)
        response = self.client.post("/settings/", data={'update_name': 'True', 'first_name': 'Gustaw'})
        self.assertTrue(response.status_code==302)
        response = self.client.post("/settings/", data={'update_lastname': 'True', 'last_name': 'Wąsowski'})
        self.assertTrue(response.status_code == 302)
        response = self.client.post("/settings/", data={'update_email': 'True', 'email': 'test@test.pl'})
        self.assertTrue(response.status_code == 302)
        response = self.client.post("/settings/", data={'update_town': 'True', 'town': 'Jelenia Góra'})
        self.assertTrue(response.status_code == 302)
        response = self.client.post("/settings/", data={'update_school': 'True', 'school': 'Szkoła'})
        self.assertTrue(response.status_code == 302)
        data = {
            "content": "This is a post, I'm testing it out",
            "image": SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }
        response = self.client.post("/settings/", data={'update_image': 'True', 'image': data})
        self.assertTrue(response.status_code == 302)
