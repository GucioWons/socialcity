from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve

from Accounts.models import Account, Post
from Accounts.views import profile_page, like_view, dislike_view


class URLTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        account = Account.objects.create(user=user)
        post = Post.objects.create(user=user)
    def test_profilepage(self):
        url = reverse('accounts:profile-view', kwargs = {'my_id': User.objects.get(username='testuser').account.pk})
        print(resolve(url))
        self.assertEquals(resolve(url).func, profile_page)
    def test_like(self):
        url = reverse('accounts:like-view', kwargs = {'my_id': Post.objects.get(user=User.objects.get(username='testuser')).pk})
        print(resolve(url))
        self.assertEquals(resolve(url).func, like_view)

    def test_like(self):
        url = reverse('accounts:dislike-view', kwargs={'my_id': Post.objects.get(user=User.objects.get(username='testuser')).pk})
        print(resolve(url))
        self.assertEquals(resolve(url).func, dislike_view)

        #url = reverse('accounts:profile-view', kwargs={'my_id': sample.pk})
        #print(resolve(url))
        #self.assertEquals(resolve(url).func, profile_page)

