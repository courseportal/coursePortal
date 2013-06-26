from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rating.ratings import INITIAL_RATING


class VoteVideo(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Submission')
	vote = models.IntegerField(default=0)

class VoteExposition(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.Exposition')
	vote = models.IntegerField(default=0)

class VoteLectureNote(models.Model):
	user = models.ForeignKey(User)
	example = models.ForeignKey('web.LectureNote')
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