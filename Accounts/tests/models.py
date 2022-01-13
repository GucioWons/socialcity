from django.contrib.auth.models import User
from django.test import TestCase

from Accounts.models import Account, Post, Notification


class TestAppModels(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("Accounts models test:")
        cls.testuser = User.objects.create_user(username='testuser', password='12345')
        cls.testaccount = Account.objects.create(user=cls.testuser)
        cls.testpost = Post.objects.create(user=cls.testuser, content='testcontent')
        cls.testnotification = Notification.objects.create(user=cls.testuser)

    def test_model_str(self):
        self.assertEqual(str(self.testaccount), 'testuser')
    def test_model_absolute(self):
        self.assertEqual('/profile/1/', self.testaccount.get_absolute_url())
    def test_model_addfriend(self):
        self.assertEqual('/add-to-friends/1/', self.testaccount.get_add_to_friends_url())
    def test_model_removefriend(self):
        self.assertEqual('/remove-from-friends/1/', self.testaccount.get_remove_from_friends_url())
    def test_model_like(self):
        self.assertEqual('/like/1/', self.testpost.get_like_url())
    def test_model_dislike(self):
        self.assertEqual('/dislike/1/', self.testpost.get_dislike_url())
    def test_model_delete(self):
        self.assertEqual('/post/delete/1/', self.testpost.get_delete_url())
    def test_post_absolute(self):
        self.assertEqual('/post/1/', self.testpost.get_absolute_url())
    def test_model_accept(self):
        self.assertEqual('/accept/1/', self.testnotification.get_accept_url())
    def test_model_decline(self):
        self.assertEqual('/decline/1/', self.testnotification.get_decline_url())

