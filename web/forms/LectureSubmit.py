from django import forms
from web.models import LectureNote

class LectureNoteForm(forms.Form):
    file = forms.FileField(label='Select a file',help_text='max. 42 megabytes')