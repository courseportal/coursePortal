from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
import random

class Assignment(models.Model):
    title = models.CharField(max_length=100, default = '')

    def __unicode__(self):
        return self.title


class Question(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='questions', default=None)
    title = models.CharField(max_length=200)
    text = models.TextField()
    solution = models.TextField() #solution script location
    numChoices = models.IntegerField()

    def __unicode__(self):
        return self.title

class QuestionChoice(models.Model):
    solution = models.TextField()
    question = models.ForeignKey(Question, related_name='choices')
    def __unicode__(self):
        return self.solution

#consider ditching all of this for a simple name field (and make him do the randomization work)
class QuestionVariable(models.Model):
    question = models.ForeignKey(Question, related_name='variables')
    name = models.CharField(max_length=100)
    VARIABLE_TYPES = (
        ('custom', 'Custom'),
        ('int', 'Integer'),
    )
    varType = models.CharField(max_length=15, choices=VARIABLE_TYPES, default='custom')
    lowerBound = models.FloatField(default=0)
    upperBound = models.FloatField(default=0)    

    def __unicode__(self):
        return self.name

    def getValue(self):
        return random.randint(self.lowerBound, self.upperBound)


class QuestionInstance(models.Model):
    title = models.CharField(max_length=200)
    solution = models.TextField()
    text = models.TextField()
    user = models.ForeignKey(User, related_name = 'questions', default = None)
    template = models.ForeignKey(Question, related_name = 'instances')
    def __unicode__(self):
        return self.user.first_name

class Choice(models.Model):
    solution = models.TextField()
    question = models.ForeignKey(QuestionInstance, related_name = 'choices')
    def __unicode__(self):
        return self.solution
