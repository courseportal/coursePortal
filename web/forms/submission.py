from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django.db.models import Q
from web.models import *
import re
from knoatom.settings import ALLOWED_FILE_EXTENTIONS, MAX_UPLOAD_SIZE
from django.template.defaultfilters import filesizeformat

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


def validate_umich_email(value):
    regex_umich_email = re.compile('\w*@umich.edu')
    if not regex_umich_email.match(value):
        raise ValidationError(u'%s is not a valid University of Michigan email address.' % value)

class testModalForm(forms.Form):
    subject = forms.CharField(max_length=100, required=True, label='Subject: ( *required)')
    content = forms.CharField(widget=forms.Textarea, required=True, label='Content: ( *required)', help_text='Flagged contents and users are reviewed by Knoatom staff 24/7 to determine whether they violate Community Guideline. Accounts are penalized for Community Guidelines violations. ')

class SubmissionForm(forms.Form):
	
	def __init__(self, *args, **kwargs):
		r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
		user = kwargs.pop('user')
		super(SubmissionForm, self).__init__(*args, **kwargs)
		if user.is_superuser:
			self.fields['classes_to_sticky_in'].queryset = Class.objects.all()
		elif user.classes_authored.exists() or user.allowed_classes.exists():
			self.fields['classes_to_sticky_in'].queryset = Class.objects.filter(Q(id__in=user.classes_authored.all()) | Q(id__in=user.allowed_classes.all()))
		else:
			self.fields['classes_to_sticky_in'].widget = forms.HiddenInput()
	
	title = forms.CharField(max_length=100, required=True)
	content = forms.CharField(widget=forms.Textarea, required=True)
	video = forms.CharField(max_length=100, validators=[validate_youtube_video_id], help_text='Please enter an 11 character YouTube video id (multiple allowed, separated by spaces). e.g. http://www.youtube.com/watch?v=VIDEO_ID')
	tags = forms.ModelMultipleChoiceField(queryset = Atom.objects.all(), widget = forms.SelectMultiple(attrs={'size':'8'}), help_text = 'Please select relevant tags for your submission.')
	
	classes_to_sticky_in = forms.ModelMultipleChoiceField(queryset = Class.objects.none(), widget = forms.SelectMultiple(attrs={'size':'8'}), required=False, help_text = 'Please select the class(es) that you want this content to be stickied in.')

	
##	def __init__(self, *args, **kwargs):
##		class_id = kwargs.pop("class_id")
##		super(SubmissionForm, self).__init__(*args, **kwargs)
##		self.fields['tags'].queryset = Atom.objects.filter(category__parent_class = class_id).distinct()

def validate_file_extension(value):
    r"""
    Checks that the file is of an allowed type set in ``knoatom/settings.py`` as ``ALLOWED_FILE_EXTENTIONS`` and file size to be under "settings.MAX_UPLOAD_SIZE".
    """
    valid = False
    for ext in ALLOWED_FILE_EXTENTIONS:
        if value.name.endswith(ext):
            if value.size < int(MAX_UPLOAD_SIZE):
                valid = True
            else:
                raise forms.ValidationError((u'Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(value.size)))
    if not valid:
        raise ValidationError(u'Not valid file type, we only accept {} files'.format(ALLOWED_FILE_EXTENTIONS))
		
def validate_link(value):
	r"""Checks that exposition links begin with ``http://`` or ``https://``.  Any links that are ``https`` probably have cross site protection though."""
	if not (re.match('^http://', value) or re.match('^https://', value)):
		raise ValidationError(u'The link must begin with http:// or https://.')

class LectureNoteForm(forms.Form):
	r"""
	This is the form for the lecture note upload system.  The ``classes_to_sticky_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in.
	
	"""
	
	def __init__(self, *args, **kwargs):
		r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
		user = kwargs.pop('user')
		super(LectureNoteForm, self).__init__(*args, **kwargs)
		if user.is_superuser:
			self.fields['classes_to_sticky_in'].queryset = Class.objects.all()
		elif user.classes_authored.exists() or user.allowed_classes.exists():
			self.fields['classes_to_sticky_in'].queryset = Class.objects.filter(Q(id__in=user.classes_authored.all()) | Q(id__in=user.allowed_classes.all()))
		else:
			self.fields['classes_to_sticky_in'].widget = forms.HiddenInput()
	
	filename = forms.CharField(max_length=200, required=True)
	file = forms.FileField(validators=[validate_file_extension], required=True)
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text='Please select the relevant atom for your submission', required=True)
	classes_to_sticky_in = forms.ModelMultipleChoiceField(queryset = Class.objects.none(), widget = forms.SelectMultiple(attrs={'size':'8'}), required=False, help_text = 'Please select the class(es) that you want this content to be stickied in.')
	
class ExampleForm(forms.Form):
	r"""
	This is the form for the example upload system.  The ``classes_to_sticky_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in.
	
	"""
	
	def __init__(self, *args, **kwargs):
		r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
		user = kwargs.pop('user')
		super(ExampleForm, self).__init__(*args, **kwargs)
		if user.is_superuser:
			self.fields['classes_to_sticky_in'].queryset = Class.objects.all()
		elif user.classes_authored.exists() or user.allowed_classes.exists():
			self.fields['classes_to_sticky_in'].queryset = Class.objects.filter(Q(id__in=user.classes_authored.all()) | Q(id__in=user.allowed_classes.all()))
		else:
			self.fields['classes_to_sticky_in'].widget = forms.HiddenInput()
	
	
	
	filename = forms.CharField(max_length=200, required=True)
	file = forms.FileField(validators=[validate_file_extension], required=True)
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text='Please select the relevant atom for your submission', required=True)
	classes_to_sticky_in = forms.ModelMultipleChoiceField(queryset = Class.objects.none(), widget = forms.SelectMultiple(attrs={'size':'8'}), required=False, help_text = 'Please select the class(es) that you want this content to be stickied in.')

class ExpoForm(forms.Form):
	r"""	
	This is the form for the exposition submit page.  The ``classes_to_sticky_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in.
	
	"""
	
	def __init__(self, *args, **kwargs):
		r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
		user = kwargs.pop('user')
		super(ExpoForm, self).__init__(*args, **kwargs)
		if user.is_superuser:
			self.fields['classes_to_sticky_in'].queryset = Class.objects.all()
		elif user.classes_authored.exists() or user.allowed_classes.exists():
			self.fields['classes_to_sticky_in'].queryset = Class.objects.filter(Q(id__in=user.classes_authored.all()) | Q(id__in=user.allowed_classes.all()))
		else:
			self.fields['classes_to_sticky_in'].widget = forms.HiddenInput()
	
	title = forms.CharField(max_length=100, required=True)
	link = forms.CharField(max_length=256, required=True, validators=[validate_link], initial="http://")
	
	atom = forms.ModelChoiceField(queryset=Atom.objects.all(), help_text= 'Please select the relevant atom for your submission', required=True)
	classes_to_sticky_in = forms.ModelMultipleChoiceField(queryset = Class.objects.none(), widget = forms.SelectMultiple(attrs={'size':'8'}), required=False, help_text = 'Please select the class(es) that you want this content to be stickied in.')