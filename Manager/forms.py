# -*- coding: utf-8 -*-
from django import forms
from HomePage.models import ImgLabel

class OptionForm(forms.Form):
    imgEditOption = []
    for obj in ImgLabel.objects.all():
        imgEditOption.append((obj.imgtype, obj.label))
    option = forms.ChoiceField(widget=forms.Select, choices=imgEditOption, label='')