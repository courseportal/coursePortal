from django.do import models

class VotableItem(models.Model):
	vote = models.IntegerField(default=0)
	
	def vote_up()