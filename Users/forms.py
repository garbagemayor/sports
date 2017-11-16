# -*- coding: utf-8 -*-
from django import forms

class EditForm(forms.Form):
    title = forms.CharField(max_length=100, label='标题')
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='内容')
