from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from Accounts.models import Comment


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
