# -*- coding: utf-8 -*-
from django import forms
from HomePage.models import Team

class OptionForm(forms.Form):
    imgEditOption = []
    for obj in Team.objects.all():
        if obj.id != 0:
            imgEditOption.append((obj.id, obj.name))
    option = forms.ChoiceField(widget=forms.Select, choices=imgEditOption, label='')