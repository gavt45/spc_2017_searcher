from django import forms

class NameForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100)