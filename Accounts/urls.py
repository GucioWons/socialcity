from django.urls import path

from Accounts.views import profile_page, add_to_friends, remove_from_friends

app_name = "accounts"
urlpatterns = [
        path('profile/<int:my_id>/', profile_page, name='profile-view'),
        path('add-to-friends/<int:my_id>/', add_to_friends, name='add-to-friends'),
        path('remove-from-friends/<int:my_id>/', remove_from_friends, name='remove-from-friends'),
    ]