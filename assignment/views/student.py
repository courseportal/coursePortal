from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from assign import index
from random import shuffle
from math import *


def grades(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url': reverse('grades'), 'title': 'Grades'})
    context = {
        'user': request.user,
        'assignment_list': assignment_list,
        'breadcrumbs': breadcrumbs,
        'grade_check': True
    }

    return render(request, 'assignment/grades.html', context)

def eval(request):
    question = QuestionInstance.objects.get(pk=request.POST['question'])
    assignment = question.assignmentInstance
    answer = request.POST['choice']
    if answer==question.solution:
        assignment.score += question.value
        assignment.save()
    question.can_edit=False
    question.save()
    return index(request)

