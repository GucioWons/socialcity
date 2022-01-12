from django import forms
from django.contrib.auth.models import User

from Accounts.models import Comment, Post, Account


class PostForm(forms.ModelForm):
    photo = forms.ImageField(label='', required=False)
    content = forms.CharField(label='',
                              error_messages={
                                  'required': 'Pole jest wymagane!'
                              },
                              widget=forms.Textarea(attrs={
                                  'rows': '5',
                                  'placeholder': 'Podziel się czymś ze światem :)'
                              }))

    class Meta:
        model = Post
        fields = ('content', 'photo')


class CommentForm(forms.ModelForm):
    content = forms.CharField()

    class Meta:
        model = Comment
        fields = ('content',)


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)


class UpdateNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name',)


class UpdateLastNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('last_name',)


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('image',)


class UpdateSchoolForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('school',)


class UpdateTownForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('town',)
