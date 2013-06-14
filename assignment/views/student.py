from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from assign import main
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
    assignment = AssignmentInstance.objects.get(pk=request.POST['assignment'])
    
    for question in assignment.questions.all():
        try:
            answer = request.POST[str(question.id)+'choice']
            if answer==question.solution:
                assignment.score += question.value
                assignment.save()
            question.can_edit=False
            question.student_answer=answer;
            question.save()
        except:
            continue
        
    if assdone(assignment):
        assignment.can_edit=False
        assignment.save()
    return main(request)

def save(request):
    assignment = AssignmentInstance.objects.get(pk=request.POST['assignment'])    
    for question in assignment.questions.all():
        try:
            answer = request.POST[str(question.id)+'choice']
            question.student_answer=answer;
            question.save()
        except:
            continue
    return main(request)

def assdone(assignment):
    for q in assignment.questions.all():
        if q.can_edit:
            return False
    return True

def list(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url': reverse('list'), 'title': 'List'})
    context = {
        'user':request.user,
        'assignment_list':assignment_list,
        'breadcrumbs':breadcrumbs,
    }
    return render(request, 'assignment/list.html',context)