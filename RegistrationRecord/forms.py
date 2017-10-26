from django import forms

from .models import Email

class PostForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ('addr', 'title', 'content')
