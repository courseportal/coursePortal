from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

class BatchAddUsersForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea, required=True, help_text='Enter a list of emails, each on a new line')
