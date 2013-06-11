from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.models import User
from assignment.models import *
from django.core.urlresolvers import reverse
from math import *
from random import shuffle


def detail(request, pk, id):
    assignmentInstance = request.user.assignmentInstances.get(pk=pk)
    question = assignmentInstance.questions.get(pk=id)
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'assignment'}]
    breadcrumbs.append({'url': reverse('assignment_detail', args=[assignmentInstance.id]), 'title': assignmentInstance})
    breadcrumbs.append({'url': reverse('question_instance', args=[assignmentInstance.id, question.id]), 'title': question})
    context = {
        'user': request.user,
    	'question_selected': question,
        'q':question,
    	'assignment_selected': assignmentInstance,
        'text': question.text,
        'choices': question.choiceInstances.all(),
        'breadcrumbs': breadcrumbs,
    }
    
    return render(request, 'question/instance.html', context)