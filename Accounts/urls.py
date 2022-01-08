from django.urls import path

from Accounts.views import profile_page

app_name = "accounts"
urlpatterns = [
        path('profile/<int:my_id>/', profile_page, name='profile-view'),
    ]