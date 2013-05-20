from datetime import datetime
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    prereq = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="postreq")
    parent = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="child")

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

class Exposition(models.Model):
    title = models.CharField(max_length=100) # title of the article or website
    link = models.CharField(max_length=100) # A URL to the location of the exposition
    cat = models.ForeignKey(Category)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title

class Submission(models.Model):
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    video = models.CharField(max_length=400, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, default=datetime.now)
    date_modified = models.DateTimeField(auto_now=True, default=datetime.now)
    tags = models.ManyToManyField(Category)

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
