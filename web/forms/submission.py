from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django.db.models import Q
import re
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.core.mail import send_mail
from web.models import Class, Content, YoutubeVideo, Link, UploadedFile

def validate_umich_email(value):
	regex_umich_email = re.compile('\w*@umich.edu')
	if not regex_umich_email.match(value):
		raise ValidationError(
			u'%s is not a valid University of Michigan email address.' % value
		)

class ReportForm(forms.Form):
	r"""Form for submitting reports."""
	subject = forms.CharField(
		max_length=100,
		required=True,
		label=_('Subject')
	)
	content = forms.CharField(
		widget=forms.Textarea,
		required=True,
		label=_('Content'),
		help_text=_('Flagged content is reviewed by Knoatom staff to determine'
			' whether it is appropiate. Accounts are penalized for Community '
			'Guidelines violations.')
	)
	contentType = forms.CharField(
		max_length=100,
		required=True,
		widget=forms.HiddenInput
	)
	contentId = forms.CharField(
		max_length=100,
		required=True,
		widget=forms.HiddenInput
	)
	
	def submit(self, user):
		r"""Submits the report to the knoatom email.  It takes in the request from the view it is submitted in."""
		subject = ("[Community Guideline Violation Report]:  " + 
			str(self.cleaned_data['subject']))
		content = ("From \"" + str(user.username) + 
			"\" : \n\nCommunity Guideline Violation Report:\t\t" + 
			str(self.cleaned_data['content'] + "\n\nContent Type:\t\t") + 
			str(self.cleaned_data['contentType']+"\n\nContent Id:\t\t") +
			str(self.cleaned_data['contentId']))
		send_mail(
			subject=subject,
			message=content,
            from_email='knoatom-noreply@umich.edu',
			recipient_list=['knoatom.webmaster@gmail.com']
		)
        
class ContentForm(forms.ModelForm):
    r"""Form for submitting content."""
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ContentForm, self).__init__(*args, **kwargs)
        if self.user.is_superuser:
            pass
        elif (self.user.classes_authored.exists() or 
              self.user.allowed_classes.exists()):
            self.fields['classes_stickied_in'].queryset = (
                Class.objects.filter(
                    Q(id__in=self.user.classes_authored.all()) | 
                    Q(id__in=self.user.allowed_classes.all())
                )
            )
        else: # If the field is empty hide the field unless user.is_superuser
            self.fields['classes_stickied_in'].widget = forms.HiddenInput()
    
    class Meta:
        model = Content
        fields = ('title', 'content_type', 'summary', 'atoms', 
            'classes_stickied_in')
            
    def save(self, commit=True):
        instance = super(ContentForm, self).save(commit=False)
        if instance.pk is None:
            instance.owner = self.user
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance
        
class YoutubeVideoForm(forms.ModelForm):
    r"""Form for submitting youtube videos."""
    def __init__(self, *args, **kwargs):
        self.content = kwargs.pop('content')
        super(YoutubeVideoForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = YoutubeVideo
        fields = ('title', 'video_id',)
        
    def save(self, commit=True):
        instance = super(YoutubeVideoForm, self).save(commit=False)
        instance.content = self.content
        if commit:
            instance.save()
        return instance
        
class LinkForm(forms.ModelForm):
    r"""Form for submitting youtube videos."""
    def __init__(self, *args, **kwargs):
        self.content = kwargs.pop('content')
        super(LinkForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Link
        fields = ('title', 'link',)
        
    def save(self, commit=True):
        instance = super(LinkForm, self).save(commit=False)
        instance.content = self.content
        if commit:
            instance.save()
        return instance
        
class UploadedFileForm(forms.ModelForm):
    r"""Form for submitting youtube videos."""
    def __init__(self, *args, **kwargs):
        self.content = kwargs.pop('content')
        super(UploadedFileForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = UploadedFile
        fields = ('title', 'file',)
        
    def save(self, commit=True):
        instance = super(UploadedFileForm, self).save(commit=False)
        instance.content = self.content
        if commit:
            instance.save()
        return instance

# class VideoForm(forms.ModelForm):
#     
#     def __init__(self, *args, **kwargs):
#         r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
#         user = kwargs.pop('user')
#         self.user = user
#         super(VideoForm, self).__init__(*args, **kwargs)
#         # Deal with classes_stickied_in
#         if user.is_superuser:
#             pass # The queryset is already Class.objects.all()
#         elif user.classes_authored.exists() or user.allowed_classes.exists():
#             self.fields['classes_stickied_in'].queryset = (
#                 Class.objects.filter(Q(id__in=user.classes_authored.all()) | 
#                 Q(id__in=user.allowed_classes.all())))
#         else: # If the field is empty hide the field unless user.is_superuser
#             self.fields['classes_stickied_in'].widget = forms.HiddenInput()
#     
#     class Meta:
#         model = Video
#         fields = ('title', 'content', 'video', 'atoms', 'classes_stickied_in')
#         
#     def save(self, commit=True):
#         instance = super(VideoForm, self).save(commit=False)
#         instance.owner = self.user
#         
#         if commit:
#             instance.save()
#             self.save_m2m()
#         
#         return instance
# 
# class NoteForm(forms.ModelForm):
#     r"""
#     This is the form for the lecture note upload system.  The ``classes_stickied_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in or if the user is a superuser.
#     
#     """
#     def __init__(self, *args, **kwargs):
#         r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
#         user = kwargs.pop('user')
#         self.user = user
#         super(NoteForm, self).__init__(*args, **kwargs)
#         # Deal with classes_stickied_in
#         if user.is_superuser:
#             pass # The queryset is already Class.objects.all()
#         elif user.classes_authored.exists() or user.allowed_classes.exists():
#             self.fields['classes_stickied_in'].queryset = (
#                 Class.objects.filter(Q(id__in=user.classes_authored.all()) | 
#                 Q(id__in=user.allowed_classes.all())))
#         else: # If the field is empty hide the field unless user.is_superuser
#             self.fields['classes_stickied_in'].widget = forms.HiddenInput()
#     
#     class Meta:
#         model = Note
#         fields = ('title', 'file', 'atoms', 'classes_stickied_in')
#         
#     def save(self, commit=True):
#         instance = super(NoteForm, self).save(commit=False)
#         instance.owner = self.user
#         
#         if commit:
#             instance.save()
#             self.save_m2m()
#         
#         return instance
#     
# class ExampleForm(forms.ModelForm):
#     r"""
#     This is the form for the example upload system.  The ``classes_stickied_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in or if the user is a superuser.
#     
#     """
#     def __init__(self, *args, **kwargs):
#         r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
#         user = kwargs.pop('user')
#         self.user = user
#         super(ExampleForm, self).__init__(*args, **kwargs)
#         # Deal with classes_stickied_in
#         if user.is_superuser:
#             pass # The queryset is already Class.objects.all()
#         elif user.classes_authored.exists() or user.allowed_classes.exists():
#             self.fields['classes_stickied_in'].queryset = (
#                 Class.objects.filter(Q(id__in=user.classes_authored.all()) | 
#                 Q(id__in=user.allowed_classes.all())))
#         else: # If the field is empty hide the field unless user.is_superuser
#             self.fields['classes_stickied_in'].widget = forms.HiddenInput()
#     
#     class Meta:
#         model = Example
#         fields = ('title', 'file', 'atoms', 'classes_stickied_in')
#         
#     def save(self, commit=True):
#         instance = super(ExampleForm, self).save(commit=False)
#         instance.owner = self.user
#         
#         if commit:
#             instance.save()
#             self.save_m2m()
#         
#         return instance
# 
# class ExpositionForm(forms.ModelForm):
#     r"""    
#     This is the form for the exposition submit page.  The ``classes_stickied_in`` is only shown if the ``user`` has any classes and is populated with the classes they are the author of or an allowed_user in or if the user is a superuser.
#     
#     """
#     def __init__(self, *args, **kwargs):
#         r"""Sets the content of ``classes_to_sticky_in`` to be classes in which the user is the ``author`` or an ``allowed_user``.  If ther user isn't authorized to change any classes then the field is hidden."""
#         user = kwargs.pop('user')
#         self.user = user
#         super(ExpositionForm, self).__init__(*args, **kwargs)
#         # Deal with classes_stickied_in
#         if user.is_superuser:
#             pass # The queryset is already Class.objects.all()
#         elif user.classes_authored.exists() or user.allowed_classes.exists():
#             self.fields['classes_stickied_in'].queryset = (
#                 Class.objects.filter(Q(id__in=user.classes_authored.all()) | 
#                 Q(id__in=user.allowed_classes.all())))
#         else: # If the field is empty hide the field unless user.is_superuser
#             self.fields['classes_stickied_in'].widget = forms.HiddenInput()
#     
#     class Meta:
#         model = Exposition
#         fields = ('title', 'link', 'atoms', 'classes_stickied_in')
#         
#     def save(self, commit=True):
#         instance = super(ExpositionForm, self).save(commit=False)
#         instance.owner = self.user
#         
#         if commit:
#             instance.save()
#             self.save_m2m()
#         
#         return instance