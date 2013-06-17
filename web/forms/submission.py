from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from web.models import *
import re
from knoatom.settings import ALLOWED_FILE_EXTENTIONS

class PlainErrorList(ErrorList):
	def __unicode__(self):
		return self.as_plain()
	def as_plain(self):
		if not self: return u''
		return u'<br/>'.join([ e for e in self ])

def validate_youtube_video_id(value):
	regex_vid_id = re.compile('[A-Za-z0-9-_]{11}')
	for v in value.split(' '):
		if not regex_vid_id.match(v):
			raise ValidationError(u'%s is not a valid YouTube video id.' % v)

class SubmissionForm(forms.Form):
	title = forms.CharField(max_length=100, required=True)
	content = forms.CharField(widget=forms.Textarea, required=True)
	video = forms.CharField(max_length=100, validators=[validate_youtube_video_id], help_text='Please enter an 11 character YouTube video id (multiple allowed, separated by spaces). e.g. http://www.youtube.com/watch?v=VIDEO_ID')
	tags = forms.ModelMultipleChoiceField(queryset = Atom.objects.all(), widget = forms.SelectMultiple(attrs={'size':'8'}), help_text = 'Please select relevant tags for your submission.')

	
##	def __init__(self, *args, **kwargs):
##		class_id = kwargs.pop("class_id")
##		super(SubmissionForm, self).__init__(*args, **kwargs)
##		self.fields['tags'].queryset = Atom.objects.filter(category__parent_class = class_id).distinct()

def validate_file_extension(value):
	r"""
	Checks that the file is of an allowed type set in ``knoatom/settings.py`` as ``ALLOWED_FILE_EXTENTIONS``.
	"""
	
	valid = False
	for ext in ALLOWED_FILE_EXTENTIONS:
		if value.name.endswith(ext):
			valid = True
	if not valid:
		raise ValidationError(u'Not valid file type, we only accept {} files'.format(ALLOWED_FILE_EXTENTIONS))
		
def validate_link(value):
	r"""Checks that exposition links begin with ``http://`` or ``https://``.  Any links that are ``https`` probably have cross site protection though."""
	if not (re.match('^http://', value) or re.match('^https://', value)):
		raise ValidationError(u'The link must begin with http:// or https://.')

class LectureNoteForm(forms.Form):
	r"""
	This is the form for the lecture note upload system.
	
	"""
	
	filename = forms.CharField(max_length=200, required=True)
	file = forms.FileField(validators=[validate_file_extension], required=True)
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text='Please select the relevant atom for your submission', required=True)
	
class ExampleForm(forms.Form):
	r"""
	This is the form for the example upload system.
	
	"""
	
	filename = forms.CharField(max_length=200, required=True)
	file = forms.FileField(validators=[validate_file_extension], required=True)
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text='Please select the relevant atom for your submission', required=True)

class ExpoForm(forms.Form):
	r"""	
	This is the form for the exposition submit page.
	
	"""
	title = forms.CharField(max_length=100, required=True)
	link = forms.CharField(max_length=256, required=True, validators=[validate_link], initial="http://")
	
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text= 'Please select the relevant atom for your submission', required=True)
	
class DeleteForm(forms.Form):
	r"""
	This is a generic form to confirm the deletion of an Exposition, LectureNote, Example or Submission.
	"""
	
	

