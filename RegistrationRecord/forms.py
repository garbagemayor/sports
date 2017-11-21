# -*- coding: utf-8 -*-
from django import forms

CONFIRM_CHOICES = (
    (True, '通过'),
    (False, '不通过'),
)
class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='')

class OptionForm(forms.Form):
    result = forms.ChoiceField(widget=forms.Select,
            choices=CONFIRM_CHOICES, label='审核意见')
