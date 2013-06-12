from django.do import models

class UserVotes(models.Model):
	user = models.OneToOneField(User, related_name="votes")
	
	example_vote_up = models.BooleanField(default=False)
	example_vote_down = models.BooleanField(default=False)