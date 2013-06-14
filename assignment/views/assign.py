from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from django.utils import simplejson as json
from random import *
from string import Template
from assignment.models import *
from math import *

def index(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
    context = {'assignment_list': assignment_list, 'user': request.user, 'breadcrumbs':breadcrumbs}

    return render(request, 'assignment_nav.html', context)

def detail(request, id):
    assignment = request.user.assignmentInstances.get(pk=id)
    question_list = assignment.questions.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url': reverse('assignment_detail', args=[assignment.id]), 'title': assignment})
    context = {
        'user':request.user,
        'assignment_list': request.user.assignmentInstances.all(),
        'assignment_selected': assignment,
        'question_list': question_list,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'assignment/detail.html', context)

def assign(request):
    user_list = User.objects.all()
    assignments = Assignment.objects.all()
    assignment_list = AssignmentInstance.objects.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('assign'), 'title':'Assign'})
    context = {
        'user': request.user,
        'users': user_list,
        'breadcrumbs': breadcrumbs,
        'assignments': assignments,
        'assignment_list': assignment_list,
    }
    return render(request, 'assignment/assign.html', context)

def instantiate(request):
    assignment = Assignment.objects.get(pk=request.POST['assignment'])
    users = User.objects.all().filter(pk=request.POST['users'])
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]

    for u in users:
        instance = AssignmentInstance(title=assignment.title, user=u, template=assignment)
        instance.save()
        for question in assignment.questions.all():
            q=question.data
            q = json.loads(q)
            q['solution']= q['solution'].replace('<br>', '\n')
            q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            for integer_index in range(len(q['choices'])):
                q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
                q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            exec q['code']
            exec q['solution']
            solution=answer
            #q text formatted here
            #shuffle(q['texts'])
            text = q['text']

            local_dict = dict(locals())
            text = Template(text).substitute(local_dict)

            # #choices formatted here
            question_instance = QuestionInstance(title=question.title, solution=solution, text=text, value=randint(0,10), assignmentInstance=instance)
            question_instance.save()
            for choice in q['choices']:
                exec choice
                choice_instance = ChoiceInstance(solution=answer, question=question_instance)
                choice_instance.save()
            if len(q['choices']) > 0:
                choice_instance = ChoiceInstance(solution=solution, question=question_instance)
                choice_instance.save()
            instance.max_score+=question_instance.value
            instance.save()
    context = {'breadcrumbs':breadcrumbs,}
    return render(request, 'assignment/instantiate.html', context)

def addA(request):
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('add_assignment'), 'title':'Add Assignment'})
    context = {'breadcrumbs':breadcrumbs}
    return render(request, 'assignment/addAssignment.html', context)

def create(request):
    a=json.loads(request.POST['assignmentdata'])
    assignment = Assignment()
    assignment.save()
    assignment.title = a["title"]
    assignment.data=a
    assignment.owners.add(request.user)
    for q in a['questions']:
        assignment.questions.add(createQ(q))
    assignment.save()
    return index(request)


def createQ(x):
    question = Question()
    question.title = x['title']
    question.data = json.dumps(x)
    question.save()
    return question