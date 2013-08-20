from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from rating.ratings import INITIAL_RATING
from rating.managers import VoteManager

class Vote(models.Model):
    r"""Model for the rating system."""
    user = models.ForeignKey(User)
    atom = models.ForeignKey("web.Atom")
    vote = models.IntegerField(default=0)
    voteUp = models.IntegerField(default=0)
    voteDown = models.IntegerField(default=0)
    content = models.ForeignKey("web.Content", blank=True, null=True, 
        editable=False, related_name='vote_set')
    # Must have only one of these fields
    #video = models.ForeignKey("web.YoutubeVideo", blank=True, null=True,
    #     editable=False, related_name='vote_set')
    #link = models.ForeignKey("web.Link", blank=True, null=True,
    #                         editable=False, related_name='vote_set')
    #file = models.ForeignKey("web.UploadedFile", blank=True, null=True,
    #                         editable=False, related_name='vote_set')
#     note = models.ForeignKey("web.Note", blank=True, null=True, 
#         editable=False, related_name='vote_set'
#     )
#     exposition = models.ForeignKey("web.Exposition", blank=True, null=True, 
#         editable=False, related_name='vote_set'
#     )
#     example = models.ForeignKey("web.Example", blank=True, null=True, 
#         editable=False, related_name='vote_set'
#     )
    topic = models.ForeignKey("pybb.Topic", blank=True, null=True, 
        editable=False, related_name='vote_set'
    )
    objects = VoteManager()
    
    def clean(self):
        r"""Make sure that this instance of Vote isn't already assigned to any content."""
        super(Vote, self).clean()
        if (getattr(self, content) is not None and
                getattr(self, topic) is not None):
            raise ValidationError("The vote can only have one of [content, topic] set and it cannot be changed once set.")

class UserRating(models.Model):
    user = models.ForeignKey(User, related_name="rating_set")
    ContentRating = models.IntegerField(default=0)
    TopicRating = models.IntegerField(default=0)
    VoteUp = models.IntegerField(default=0)
    VoteDown = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    
@receiver(post_save, sender=User)
def create_uservotes(sender, **kwargs):
    if not UserRating.objects.filter(user=kwargs['instance']).exists():
        UserRating.objects.create(user=kwargs['instance'], rating=INITIAL_RATING)