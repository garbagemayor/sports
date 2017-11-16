from django import forms

class EditForm(forms.Form):
    title = forms.CharField(max_length=100, label='标题')
    content = forms.CharField(widget=forms.Textarea(attrs={'id': 'editor'}), label='内容')
    result = forms.BooleanField(required=False, label='审核结果')
