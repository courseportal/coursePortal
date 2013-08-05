from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, Textarea
from django.utils import simplejson as json
from django.utils import timezone

class Question(models.Model):
    title = models.CharField(max_length=200)
    owners = models.ManyToManyField(User, related_name='owned_questions', blank=True, null=True)
    atoms = models.ManyToManyField("web.Atom", related_name='related_questions', blank=True, null=True)
    data = models.TextField()
    numCorrect = models.IntegerField(default = 0)
    numIncorrect = models.IntegerField(default = 0)
    isCopy = models.BooleanField(default = False)
    original = models.ForeignKey('Question', blank=True, null=True, related_name = 'copy', on_delete = models.SET_NULL)

    def get_rating(self):
        if self.numCorrect+self.numIncorrect < 10:
            return "Untested"
        ratio = float(self.numCorrect/float(self.numCorrect+self.numIncorrect))
        if ratio >= .75:
            return "easy"
        elif ratio >= .5:
            return "medium"
        elif ratio >= .25:
            return "hard"
        else:
            return "very hard"
    def __unicode__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=100, default = '')
    due_date = models.DateTimeField()
    start_date = models.DateTimeField()
    isCopy = models.BooleanField(default=False)
    data = models.TextField(default='', null=True, blank=True)
    questions = models.ManyToManyField(Question, related_name='assigned_to')
    owners = models.ManyToManyField(User, related_name='owned_assignments', blank=True, null=True)
    def __unicode__(self):
        return self.title

class AssignmentInstance(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name = 'assignmentInstances')
    template = models.ForeignKey(Assignment, related_name = 'instances')
    can_edit = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    score = models.FloatField(default = 0.0)
    max_score = models.FloatField(default = 0.0)
    def __unicode__(self):
        return self.title
    def was_published(self):
        return self.start_date <= timezone.now()
    def was_due(self):
        return self.due_date <= timezone.now()


class QuestionInstance(models.Model):
    title = models.CharField(max_length=200)
    solution = models.TextField()
    text = models.TextField()
    value = models.FloatField(default = 1.0)
    can_edit = models.BooleanField(default=True)
    student_answer = models.TextField(default = "")
    assignmentInstance = models.ForeignKey(AssignmentInstance, related_name='questions', default = None)
    template = models.ForeignKey(Question, related_name='instances', default= None)
    def __unicode__(self):
        return self.title
    def was_published(self):
        return self.assignmentInstance.start_date <= timezone.now()
    def was_due(self):
        return self.assignmentInstance.due_date <= timezone.now()

class ChoiceInstance(models.Model):
    solution = models.TextField()
    question = models.ForeignKey(QuestionInstance, related_name = 'choiceInstances')
    def __unicode__(self):
        return self.solution


class Variable(models.Model):
    name = models.CharField(max_length=200)
    variables = models.TextField(blank=True)
    validation_code = models.TextField(default="result=0")
    generated_code = models.TextField(blank=True)
    def __unicode__(self):
        return self.name
