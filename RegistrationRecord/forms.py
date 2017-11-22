# -*- coding: utf-8 -*-
from django import forms

passExamineOption = (
    (1, '通过审核'),
    (2, '拒绝通过审核'),
)
emailOrNoteOption = (
    (1, "仅发送站内信"),
    (2, "仅发送邮件"),
    (3, "发送站内信和邮件"),
    (4, "不发送任何消息"),
)
sendMessageOption = (
    (1, "仅发送给队长"),
    (2, "发送给全队"),
)
class EditForm(forms.Form):
    passExamineSelector = forms.ChoiceField(widget=forms.Select, choices=passExamineOption, label='审核结果')
    emailOrNoteSelector = forms.ChoiceField(widget=forms.Select, choices=emailOrNoteOption, label='审核消息类型')
    sendMessageSelector = forms.ChoiceField(widget=forms.Select, choices=sendMessageOption, label='审核消息对象')
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='')
