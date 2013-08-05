from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from rating.ratings import INITIAL_RATING

class Vote(models.Model):
	r"""Model for the rating system."""
	user = models.ForeignKey(User)
	atom = models.ForeignKey("web.Atom")
	vote = models.IntegerField(default=0)
	# Must have only one of these fields
	video = models.ForeignKey("web.Video", blank=True, null=True,
		editable=False
	)
	note = models.ForeignKey("web.Note", blank=True, null=True, 
        editable=False, related_name='vote_set'
    )
	exposition = models.ForeignKey("web.Exposition", blank=True, null=True, 
		editable=False, related_name='vote_set'
	)
	example = models.ForeignKey("web.Example", blank=True, null=True, 
		editable=False, related_name='vote_set'
	)
	topic = models.ForeignKey("pybb.Topic", blank=True, null=True, 
		editable=False, related_name='vote_set'
	)
	
	def clean(self):
		r"""Make sure that this instance of Vote isn't already assigned to any content."""
		super(Vote, self).clean()
		content_is_not_none = [(lambda x: getattr(vote, x.name)
			is not None)(x) for x in vote._meta.fields[4:]]
		if content_is_not_none.count(True) != 0:
			raise ValidationError("The vote can only have one of [video, note, exposition, example, topic] set and it cannot be changed once set.")
		

class VoteVideo(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Video')
	vote = models.IntegerField(default=0)

class VoteExposition(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Exposition')
	vote = models.IntegerField(default=0)

class VoteNote(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Note')
	vote = models.IntegerField(default=0)

class VoteExample(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Example')
	vote = models.IntegerField(default=0)
	
class VoteTopic(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('pybb.Topic')
	vote = models.IntegerField(default=0)
	
class UserRating(models.Model):
	user = models.ForeignKey(User, related_name="rating_set")
	ExpoRating = models.IntegerField(default=0)
	LecNoteRating = models.IntegerField(default=0)
	ExampleRating = models.IntegerField(default=0)
	VideoRating = models.IntegerField(default=0)
	TopicRating = models.IntegerField(default=0)
	VoteUp = models.IntegerField(default=0)
	VoteDown = models.IntegerField(default=0)
	rating = models.IntegerField(default=0)
	
@receiver(post_save, sender=User)
def create_uservotes(sender, **kwargs):
	if not UserRating.objects.filter(user=kwargs['instance']).exists():
		UserRating.objects.create(user=kwargs['instance'], rating=INITIAL_RATING)