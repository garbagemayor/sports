from django import forms

class EmailForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    result = forms.BooleanField(required=False)
