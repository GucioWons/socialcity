from django.contrib.auth.models import User
from django.test import TestCase

from django.test.client import Client
# Create your tests here.
from django.urls import reverse, resolve

from Pages.views import home_page, login_page, register_page, logout_view, landing_page, search_page, notification_page, \
    settings_page


class URLTests(TestCase):
    def test_testhomepage(self):
        url = reverse('pages:home-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home_page)
    def test_loginpage(self):
        url = reverse('pages:login-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, login_page)
    def test_registerpage(self):
        url = reverse('pages:register-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, register_page)
    def test_logoutpage(self):
        url = reverse('pages:logout-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logout_view)
    def test_landingpage(self):
        url = reverse('pages:landing-view')
        print(resolve(url))
        self.assertEquals(resolve(url).func, landing_page)
    def test_searchpage(self):
        url = reverse('pages:search-page')
        print(resolve(url))
        self.assertEquals(resolve(url).func, search_page)
    def test_notifiactionpage(self):
        url = reverse('pages:notification-page')
        print(resolve(url))
        self.assertEquals(resolve(url).func, notification_page)
    def test_settingspage(self):
        url = reverse('pages:settings-page')
        print(resolve(url))
        self.assertEquals(resolve(url).func, settings_page)