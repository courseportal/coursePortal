from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from haystack import indexes
from django.db.models.signals import pre_delete, post_delete, pre_save, post_save
from django.dispatch import receiver
from knoatom.settings import MEDIA_ROOT
from web.rating import *
from subprocess import Popen


STATUS_CHOICES = (
	('A', 'Active'),
	('N', 'Not active'),
)

class BaseCategory(models.Model):
	name = models.CharField(max_length=200)
	summary = models.TextField(default="There is no summary added at this time.")
	child_categories = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="parent_categories")

	class Meta:
		ordering = ['name']
		verbose_name_plural = "Base Categories"

	def __unicode__(self):
		return self.name

class Atom(models.Model):
	name = models.CharField(max_length=200)
	summary = models.TextField(default="There is no summary added at this time.")
	base_category = models.ForeignKey(BaseCategory, related_name = "child_atoms")
	#prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name
		
class Submission(models.Model):
    owner = models.ForeignKey(User, related_name="video_owner")
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.CharField(max_length=400, blank=True, help_text ="Please enter an 11 character YouTube VIDEO_ID   or  enter [\"VIDEO_ID\"] directly. (e.g. http://www.youtube.com/watch?v=VIDEO_ID) ")
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Atom, related_name="tags")
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title  

class VoteCategory(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ['name']
		verbose_name_plural = "Vote categories"

	def __unicode__(self):
		return self.name

class Vote(models.Model):
	user = models.ForeignKey(User)
	submission = models.ForeignKey(Submission, related_name='votes_s')
	v_category = models.ForeignKey(VoteCategory, related_name='votes_s')
	rating = models.IntegerField()
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s: %s: %s' % (self.user, self.submission.title, self.v_category.name)

class Exposition(models.Model):
	title = models.CharField(max_length=100) # title of the article or website
	link = models.CharField(max_length=100) # A URL to the location of the exposition
	atom = models.ForeignKey(Atom)
	owner = models.ForeignKey(User, related_name="exposition_set")
	votes = models.IntegerField(default=0)
	
	class Meta:
		ordering = ['title']
	
	def __unicode__(self):
		return self.title


#Lecture Note
class LectureNote(models.Model):
    file = models.FileField(upload_to='lecture_notes/')
    owner = models.ForeignKey(User, related_name="lecturenote_set")
    filename = models.CharField(max_length=200)
    atom = models.ForeignKey(Atom, related_name = "lecturenote_set")
    votes = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now=True)

	
    def __unicode__(self):
        return self.filename
        


class Example(models.Model):
	file = models.FileField(upload_to='examples/')
	owner = models.ForeignKey(User, related_name="example_set")
	filename = models.CharField(max_length=200)
	atom = models.ForeignKey(Atom, related_name = "example_set")
	date_created = models.DateTimeField(auto_now=True)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.filename

class Class(models.Model):
	r"""
	This is the model for the class feature of the site which allows professors to create their own class pages which they can customize to fit their needs.  They can sticky content to force that material to stay at the top of the content display lists.
	
	"""
	name = models.CharField(max_length=100)
	allowed_users = models.ManyToManyField(User, blank=True, related_name='allowed_classes')
	students = models.ManyToManyField(User, blank=True, related_name = 'enrolled_classes')
	author = models.ForeignKey(User, related_name = 'classes_authored')
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
	summary = models.TextField(default="There is no summary added at this time.")
	
	# Stickied Content
	stickied_videos = models.ManyToManyField(Submission, blank=True, related_name='classes_stickied_in')
	stickied_expos = models.ManyToManyField(Exposition, blank=True, related_name='classes_stickied_in')
	stickied_notes = models.ManyToManyField(LectureNote, blank=True, related_name='classes_stickied_in')
	stickied_examples = models.ManyToManyField(Example, blank=True, related_name = 'classes_stickied_in')
	
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['name']
		verbose_name_plural = "Classes"

class AtomCategory(models.Model):
	name = models.CharField(max_length=200)
	parent_class = models.ForeignKey(Class)
	child_categories = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="parent_categories")
	child_atoms = models.ManyToManyField(Atom, blank=True, symmetrical=False)
	class Meta:
		ordering = ['name']
		verbose_name_plural = "Categories"

	def __unicode__(self):
		return self.name
		
class VoteVideo(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey(Submission)
	vote = models.IntegerField(default=0)

class VoteExposition(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey(Exposition)
	vote = models.IntegerField(default=0)

class VoteLectureNote(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey(LectureNote)
	vote = models.IntegerField(default=0)

class VoteExample(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey(Example)
	vote = models.IntegerField(default=0)
	
class UserRating(models.Model):
    user = models.ForeignKey(User, related_name="rating_set")
    ExpoRating = models.IntegerField(default=0)
    LecNoteRating = models.IntegerField(default=0)
    ExampleRating = models.IntegerField(default=0)
    VideoRating = models.IntegerField(default=0)
    VoteUp = models.IntegerField(default=0)
    VoteDown = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
	
	
@receiver(post_save, sender=User)
def create_uservotes(sender, **kwargs):
	if not UserRating.objects.filter(user=kwargs['instance']).exists():
		UserRating.objects.create(user=kwargs['instance'], rating=INITIAL_RATING)

@receiver(post_save, sender=Submission)
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

@receiver(post_save, sender=LectureNote)
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

@receiver(pre_delete, sender=Submission)
def delete_video_rate(sender, **kwargs):
    user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
    user_rate.VideoRating -= video_object_delta_rating()
    user_rate.rating -= video_object_delta_rating()
    user_vote = VoteVideo.objects.filter(example=kwargs['instance'])
    for v in user_vote:
        if v.vote == vote_up_delta_rating():
            user_rate.VoteUp -= vote_up_delta_rating()
            user_rate.rating -= vote_up_delta_rating()
        elif v.vote == vote_down_delta_rating():
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
    user_vote = VoteExposition.objects.filter(example=kwargs['instance'])
    for v in user_vote:
        if v.vote == vote_up_delta_rating():
            user_rate.VoteUp -= vote_up_delta_rating()
            user_rate.rating -= vote_up_delta_rating()
        elif v.vote == vote_down_delta_rating():
            user_rate.VoteDown -= vote_down_delta_rating()
            user_rate.rating -= vote_down_delta_rating()
    user_rate.save()



@receiver(pre_delete, sender=LectureNote)
def delete_note_rate(sender, **kwargs):
    """
        This adds the functionality to remove the file upon deletion.
    """
    print("*******************")
    print(kwargs['instance'].file)
    print("*******************")
    kwargs['instance'].file.delete()
    user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
    user_rate.LecNoteRating -= note_object_delta_rating()
    user_rate.rating -= note_object_delta_rating()
    user_vote = VoteLectureNote.objects.filter(example=kwargs['instance'])
    for v in user_vote:
        if v.vote == vote_up_delta_rating():
            user_rate.VoteUp -= vote_up_delta_rating()
            user_rate.rating -= vote_up_delta_rating()
        elif v.vote == vote_down_delta_rating():
            user_rate.VoteDown -= vote_down_delta_rating()
            user_rate.rating -= vote_down_delta_rating()
    user_rate.save()


@receiver(pre_delete, sender=Example)
def delete_example_rate(sender, **kwargs):
    """
    This adds the functionality to remove the file upon deletion.
    """
    print("*******************")
    print(kwargs['instance'].file)
    print("*******************")
    kwargs['instance'].file.delete()
    user_rate = UserRating.objects.get(user=kwargs['instance'].owner)
    user_rate.ExampleRating -= example_object_delta_rating()
    user_rate.rating -= example_object_delta_rating()
    user_vote = VoteExample.objects.filter(example=kwargs['instance'])
    for v in user_vote:
        if v.vote == vote_up_delta_rating():
            user_rate.VoteUp -= vote_up_delta_rating()
            user_rate.rating -= vote_up_delta_rating()
        elif v.vote == vote_down_delta_rating():
            user_rate.VoteDown -= vote_down_delta_rating()
            user_rate.rating -= vote_down_delta_rating()
    user_rate.save()

#bugReport
class BugReport(models.Model):
	subject = models.CharField(max_length=100)
	content = models.TextField()
	email = models.EmailField()
	cc_myself = models.BooleanField(default=False)
	def __unicode__(self):
		return self.subject
	class Meta:
		ordering = ['subject']
		verbose_name_plural = "BugReports"

	
