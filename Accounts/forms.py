from django import forms

from Accounts.models import Comment, Post


class PostForm(forms.ModelForm):
    photo = forms.ImageField(label='',required=False)
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
