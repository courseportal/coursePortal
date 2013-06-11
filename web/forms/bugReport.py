from django import forms
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
import re

class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

def validate_umich_email(value):
    regex_umich_email = re.compile('\w*@umich.edu')
    if not regex_umich_email.match(value):
        raise ValidationError(u'%s is not a valid University of Michigan email address.' % value)

class bugReportForm(forms.Form):
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(max_length=100, required=True, validators=[validate_umich_email], help_text='Only University of Michigan email addresses are currently allowed to be used.')
    cc_myself = forms.BooleanField(required=False)



