from django.urls import path

from Pages.views import home_page, register_page, login_page, landing_page

app_name = "pages"
urlpatterns = [
        path('', home_page, name='home-view'),
        path('login/', login_page, name='login-view'),
        path('register/', register_page, name='register-view'),
        path('landing/', landing_page, name='ladning-view'),
    ]