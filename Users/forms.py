# -*- coding: utf-8 -*-
from django import forms

class EditForm(forms.Form):
    title = forms.CharField(max_length=None, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='')
