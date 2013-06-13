from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from haystack import indexes
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from knoatom.settings import MEDIA_ROOT
from rating.models import UserVotes

STATUS_CHOICES = (
    ('A', 'Active'),
    ('N', 'Not active'),
)

class Class(models.Model):
    name = models.CharField(max_length=100)
    allowed_users = models.ManyToManyField(User, blank=True, related_name='allowed_classes')
    students = models.ManyToManyField(User, blank=True, related_name = 'enrolled_classes')
    author = models.ForeignKey(User, related_name = 'author')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='N')
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Classes"

class BaseCategory(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    child_categories = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="parent_categories")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Base Categories"

    def __unicode__(self):
        return self.name

class Atom(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField()
    base_category = models.ForeignKey(BaseCategory, related_name = "child_atoms")
    #prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

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
    
class Exposition(models.Model):
    title = models.CharField(max_length=100) # title of the article or website
    link = models.CharField(max_length=100) # A URL to the location of the exposition
    atom = models.ForeignKey(Atom)
    owner = models.ForeignKey(User)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Submission(models.Model):
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.CharField(max_length=400, blank=True, help_text ="Please enter an 11 character YouTube VIDEO_ID   or  enter [\"VIDEO_ID\"] directly. (e.g. http://www.youtube.com/watch?v=VIDEO_ID) ")
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Atom, related_name="tags")

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
    submission = models.ForeignKey(Submission, related_name='votes')
    v_category = models.ForeignKey(VoteCategory, related_name='votes')
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s: %s: %s' % (self.user, self.submission.title, self.v_category.name)

#Lecture Note
class LectureNote(models.Model):
	file = models.FileField(upload_to=MEDIA_ROOT+'/lecture_notes/')
	owner = models.ForeignKey(User)
	filename = models.CharField(max_length=200)
	atom = models.ForeignKey(Atom, related_name = "lecturenote_set")
	date_created = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return self.filename
		
class Example(models.Model):
	file = models.FileField(upload_to=MEDIA_ROOT+'/examples/')
	owner = models.ForeignKey(User)
	filename = models.CharField(max_length=200)
	atom = models.ForeignKey(Atom, related_name = "example_set")
	date_created = models.DateTimeField(auto_now=True)
	
	user_votes = models.ManyToManyField(UserVotes)
	votes = models.IntegerField(default=0)

	#user_votes = example.user_votes.get(user=user)
	
	def __unicode__(self):
		return self.filename
		
@receiver(pre_delete, sender=LectureNote)
def delete_note_file(sender, **kwargs):
	r"""
	This adds the functionality to remove the file upon deletion.
	"""
	
	kwargs['instance'].file.delete()
	
@receiver(pre_delete, sender=Example)
def delete_example_file(sender, **kwargs):
	r"""
	This adds the functionality to remove the file upon deletion.
	"""
	
	kwargs['instance'].file.delete()

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

    
