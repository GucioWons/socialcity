from django.urls import path

from Accounts.views import profile_page, add_to_friends, remove_from_friends, like_view, dislike_view, accept_request, \
        decline_request

app_name = "accounts"
urlpatterns = [
        path('profile/<int:my_id>/', profile_page, name='profile-view'),
        path('add-to-friends/<int:my_id>/', add_to_friends, name='add-to-friends'),
        path('remove-from-friends/<int:my_id>/', remove_from_friends, name='remove-from-friends'),
        path('like/<int:my_id>/', like_view, name='like-view'),
        path('dislike/<int:my_id>/', dislike_view, name='dislike-view'),
        path('accept/<int:my_id>/', accept_request, name='accept-view'),
        path('decline/<int:my_id>/', decline_request, name='decline-view'),
    ]