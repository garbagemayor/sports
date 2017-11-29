# -*- coding: utf-8 -*-
from django import forms

imgEditOption = (
    (1, '设为首页背景'),
    (2, '设为风采展示'),
    (3, '撤回'),
    (4, '删除'),
    (5, '系队'),
    (6, '名人堂'),
)

class EditForm(forms.Form):
    title = forms.CharField(max_length=None, label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='')

class OptionForm(forms.Form):
    option = forms.ChoiceField(widget=forms.Select, choices=imgEditOption, label='')