from django import forms

from Posts.models import Post


class PostForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
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
