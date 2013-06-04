from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, Textarea
import random


class Question(models.Model):
    title = models.CharField(max_length=200)
    data = models.TextField()
    def __unicode__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=100, default = '')
    questions = models.ManyToManyField(Question)
    owners = models.ManyToManyField(User, related_name='templates', blank=True, null=True)
    def __unicode__(self):
        return self.title

class AssignmentInstance(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name = 'assignmentInstances')
    template = models.ForeignKey(Assignment, related_name = 'instances')
    score = models.FloatField(default = 0)
    max_score = models.FloatField(default = 0)
    def __unicode__(self):
        return self.title


class QuestionInstance(models.Model):
    title = models.CharField(max_length=200)
    solution = models.TextField()
    text = models.TextField()
    value = models.FloatField(default = 1.0)
    assignmentInstance = models.ForeignKey(AssignmentInstance, related_name='questions', default = None)
    def __unicode__(self):
        return self.title

class ChoiceInstance(models.Model):
    solution = models.TextField()
    question = models.ForeignKey(QuestionInstance, related_name = 'choiceInstances')
    def __unicode__(self):
        return self.solution