from datetime import datetime
import re
from django.contrib.auth.models import User
from django.db import models
from haystack import indexes
from django.http import Http404
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from knoatom.settings import MEDIA_ROOT, ALLOWED_FILE_EXTENTIONS, \
	MAX_UPLOAD_SIZE
from rating.models import *
from rating.ratings import *



STATUS_CHOICES = (
	('A', 'Active'),
	('N', 'Not active'),
)

class BaseCategory(models.Model):
	title = models.CharField(max_length=200)
	summary = models.TextField(
		default="There is currently no summary."
	)
	parent_categories = models.ManyToManyField(
		"self",
		blank=True,
		symmetrical=False,
		related_name="child_categories"
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)

	class Meta:
		ordering = ['title']
		verbose_name_plural = _("Base Categories")

	def __unicode__(self):
		return self.title

class Atom(models.Model):
	title = models.CharField(max_length=200)
	summary = models.TextField(
		default=_("There is no summary added at this time.")
	)
	base_category = models.ForeignKey(BaseCategory,
		related_name="child_atoms"
	)
	#prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
	class Meta:
		ordering = ['title']

	def __unicode__(self):
		return self.title
		
# Validator for video	
def validate_youtube_video_id(value):
	regex_vid_id = re.compile('[A-Za-z0-9-_]{11}')
	if not regex_vid_id.match(value):
		raise ValidationError('%s is not a valid YouTube video id.' % value)
		
class Video(models.Model):
	owner = models.ForeignKey(User, related_name="video_owner")
	title = models.CharField(max_length=200)
	content = models.TextField()
	video = models.CharField(
		max_length=400,
		blank=True,
		help_text=_("Please enter an 11 character YouTube VIDEO_ID (e.g. "
			"http://www.youtube.com/watch?v=VIDEO_ID)"), 		
		validators=[validate_youtube_video_id],
	)
	atoms = models.ManyToManyField(Atom, related_name="video_set")
	classes_stickied_in = models.ManyToManyField(
		"Class",
		blank=True,
		related_name='stickied_videos',
		help_text=_('Please select the class(es) that you want this content '
			'to be stickied in.')
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
	
	class Meta:
		ordering = ['title']

	def __unicode__(self):
		return self.title
# Validator for expositions
def validate_link(value):
	r"""Checks that exposition links begin with ``http://`` or ``https://``.  Any links that are ``https`` probably have cross site protection though."""
	if not (re.match('^http://', value) or re.match('^https://', value)):
		raise ValidationError(u'The link must begin with http:// or https://.')

class Exposition(models.Model):
	title = models.CharField(max_length=100) # title of the article or website
	link = models.CharField(max_length=100, validators=[validate_link], default="http://")
	atoms = models.ManyToManyField(Atom, related_name="exposition_set")
	owner = models.ForeignKey(User, related_name="exposition_set")
	classes_stickied_in = models.ManyToManyField(
		"Class",
		blank=True,
		related_name='stickied_expositions',
		help_text=_('Please select the class(es) that you want this content '
			'to be stickied in.')
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
	
	class Meta:
		ordering = ['title']
	
	def __unicode__(self):
		return self.title
		
# Validator for Note and Example
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

#Lecture Note
class Note(models.Model):
	file = models.FileField(
		upload_to='notes/',
		validators=[validate_file_extension]
	)
	owner = models.ForeignKey(User, related_name="note_set")
	title = models.CharField(max_length=200)
	atoms = models.ManyToManyField(Atom, related_name = "note_set")
	classes_stickied_in = models.ManyToManyField(
		"Class",
		blank=True,
		related_name='stickied_notes',
		help_text=_('Please select the class(es) that you want this content '
			'to be stickied in.')
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)

	class Meta:
		ordering = ['title']
	
	def __unicode__(self):
		return self.title
		


class Example(models.Model):
	file = models.FileField(
		upload_to='examples/',
		validators=[validate_file_extension]
	)
	owner = models.ForeignKey(User, related_name="example_set")
	title = models.CharField(max_length=200)
	atoms = models.ManyToManyField(Atom, related_name = "example_set")
	classes_stickied_in = models.ManyToManyField(
		"Class",
		blank=True,
		related_name='stickied_examples',
		help_text=_('Please select the class(es) that you want this content '
			'to be stickied in.')
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)

	class Meta:
		ordering = ['title']

	def __unicode__(self):
		return self.title

class Class(models.Model):
	r"""
	This is the model for the class feature of the site which allows professors to create their own class pages which they can customize to fit their needs.  They can sticky content to force that material to stay at the top of the content display lists.
	
	"""
	title = models.CharField(verbose_name=_('Class Name'), max_length=100)
	instructors = models.ManyToManyField(
		User,
		verbose_name=_('Instructors'),
		blank=True,
		related_name='allowed_classes'
	)
	students = models.ManyToManyField(
		User,
		verbose_name=_('Students'),
		blank=True,
		related_name='enrolled_classes'
	)
	owner = models.ForeignKey(
		User,
		verbose_name=_('Professor'),
		related_name = 'classes_authored'
	)
	status = models.CharField(
		verbose_name=_('Status'),
		max_length=1,
		choices=STATUS_CHOICES,
		default='N'
	)
	summary = models.TextField(
		verbose_name=_('Class Description'),
		default="There is no summary added at this time."
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
	
	
	def __unicode__(self):
		return self.title
		
	class Meta:
		ordering = ['title']
		verbose_name_plural = _("Classes")
		
	def get_absolute_url(self):
		if self.pk is not None:
			return reverse('classes', args=[self.pk])
		else:
			raise Http404

class ClassCategory(models.Model):
	title = models.CharField(verbose_name=_('Category Name'), max_length=200)
	parent_class = models.ForeignKey(
		Class,
		default=None,
		blank=True,
		null=True,
		related_name="category_set"
	)
	parent_categories = models.ManyToManyField(
		"self",
		blank=True,
		symmetrical=False,
		related_name="child_categories"
	)
	child_atoms = models.ManyToManyField(
		Atom,
		blank=True,
		related_name="categories"
	)
	
	date_created = models.DateTimeField(
		auto_now_add=True,
		default=datetime.now
	)
	date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
	
	class Meta:
		ordering = ['title']
		verbose_name_plural = _("Categories")

	def __unicode__(self):
		return self.title
		
@receiver(post_save, sender=Video)
def add_submission_rate(sender, **kwargs):
	if kwargs['created']:
		user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
		user_rate.VideoRating += video_object_delta_rating()
		user_rate.rating += video_object_delta_rating()
		user_rate.save()


@receiver(post_save, sender=Exposition)
def add_expo_rate(sender, **kwargs):
	if kwargs['created']:
		user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
		user_rate.ExpoRating += expo_object_delta_rating()
		user_rate.rating += expo_object_delta_rating()
		user_rate.save()

@receiver(post_save, sender=Note)
def add_note_rate(sender, **kwargs):
	if kwargs['created']:
		user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
		user_rate.LecNoteRating += note_object_delta_rating()
		user_rate.rating += note_object_delta_rating()
		user_rate.save()

@receiver(post_save, sender=Example)
def add_example_rate(sender, **kwargs):
	if kwargs['created']:
		user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
		user_rate.ExampleRating += example_object_delta_rating()
		user_rate.rating += example_object_delta_rating()
		user_rate.save()

@receiver(pre_delete, sender=Video)
def delete_video_rate(sender, **kwargs):
	user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
	user_rate.VideoRating -= video_object_delta_rating()
	user_rate.rating -= video_object_delta_rating()
	user_vote = Vote.objects.filter(video=kwargs['instance'])
	for v in user_vote:
		if v.vote > 0:
			user_rate.VoteUp -= vote_up_delta_rating()
			user_rate.rating -= vote_up_delta_rating()
		elif v.vote < 0:
			user_rate.VoteDown -= vote_down_delta_rating()
			user_rate.rating -= vote_down_delta_rating()
	user_rate.save()


@receiver(pre_delete, sender=Exposition)
def delete_exposition_rate(sender, **kwargs):
	"""
	This adds the functionality to remove the file upon deletion.
	"""
	user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
	user_rate.ExpoRating -= expo_object_delta_rating()
	user_rate.rating -= expo_object_delta_rating()
	user_vote = Vote.objects.filter(exposition=kwargs['instance'])
	for v in user_vote:
		if v.vote > 0:
			user_rate.VoteUp -= vote_up_delta_rating()
			user_rate.rating -= vote_up_delta_rating()
		elif v.vote < 0:
			user_rate.VoteDown -= vote_down_delta_rating()
			user_rate.rating -= vote_down_delta_rating()
	user_rate.save()



@receiver(pre_delete, sender=Note)
def delete_note_rate(sender, **kwargs):
	"""
	This adds the functionality to remove the file upon deletion.
	"""
	kwargs['instance'].file.delete()
	user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
	user_rate.LecNoteRating -= note_object_delta_rating()
	user_rate.rating -= note_object_delta_rating()
	user_vote = Vote.objects.filter(note=kwargs['instance'])
	for v in user_vote:
		if v.vote > 0:
			user_rate.VoteUp -= vote_up_delta_rating()
			user_rate.rating -= vote_up_delta_rating()
		elif v.vote < 0:
			user_rate.VoteDown -= vote_down_delta_rating()
			user_rate.rating -= vote_down_delta_rating()
	user_rate.save()


@receiver(pre_delete, sender=Example)
def delete_example_rate(sender, **kwargs):
	"""
	This adds the functionality to remove the file upon deletion.
	"""
	kwargs['instance'].file.delete()
	user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
	user_rate.ExampleRating -= example_object_delta_rating()
	user_rate.rating -= example_object_delta_rating()
	user_vote = Vote.objects.filter(example=kwargs['instance'])
	for v in user_vote:
		if v.vote > 0:
			user_rate.VoteUp -= vote_up_delta_rating()
			user_rate.rating -= vote_up_delta_rating()
		elif v.vote < 0:
			user_rate.VoteDown -= vote_down_delta_rating()
			user_rate.rating -= vote_down_delta_rating()
	user_rate.save()
