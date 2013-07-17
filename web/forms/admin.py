from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList

class BatchAddUsersForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea, required=True, help_text='Enter a list of emails, each on a new line')
