from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from knoatom.view_functions import get_breadcrumbs
from assignment.views.question import detail
from web.models import Atom
from assign import main
from random import shuffle, randint
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
            #Store student answer
            answer = request.POST[str(question.id)+'choice']
            question.can_edit=False
            question.student_answer=answer;
            question.save()

            template = question
            if template.isCopy == True:
                template = template.original
            if answer==question.solution:
                assignment.score += question.value
                assignment.save()
                if not template == None:
                    template.numCorrect+=1
                    template.save()
            elif not template == None:
                template.numIncorrect+=1
                template.save()
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
    return render(request, 'assignment/instancelist.html',context)


def choose_atom(request, messages=False):
    context = get_breadcrumbs(request.path)
    context['atom_list'] = Atom.objects.all()
    if messages:
        context['messages'] = messages
    return render(request, 'atomList.html', context)

def practice(request, id):
    context = get_breadcrumbs(request.path)
    question_list = Atom.objects.get(id=id).related_questions.all()
    count = question_list.count()
    if count==0:
        messages = ['No Questions related to that atom!']
        return choose_atom(request, messages)
    question = question_list[randint(0,count-1)]
    #generate question
    qdat = detail(request, question.id, True)
    #load page
    context['qid'] = question.id
    context['atomid'] = id
    context['title'] = question.title
    context['text'] = qdat['text']
    context['answer'] = qdat['answer']
    context['choices'] = qdat['choices']
    return render(request, 'question/practice.html', context)



