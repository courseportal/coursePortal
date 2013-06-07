from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from django.utils import simplejson as json
from random import *
from string import Template
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
            q = json.loads(question.data)
            for integer_index in range(len(q['solutions'])):
                q['solutions'][integer_index]= q['solutions'][integer_index].replace('<br>', '\n')
                q['solutions'][integer_index] = q['solutions'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            exec q['solutions'][0]
            solution = answer

            #q text formatted here
            shuffle(q['texts'])
            text = q['texts'][0]

            local_dict = dict(locals())
            text = Template(text).substitute(local_dict)

            # #choices formatted here
            question_instance = QuestionInstance(title=question.title, solution=solution, text=text, value=randint(0,10), assignmentInstance=instance)
            question_instance.save()
            q['solutions'].pop(0)
            for choice in q['solutions']:
                exec choice
                choice_instance = ChoiceInstance(solution=answer, question=question_instance)
                choice_instance.save()
            if len(q['solutions']) > 0:
                choice_instance = ChoiceInstance(solution=solution, question=question_instance)
                choice_instance.save()
            instance.max_score+=question_instance.value
            instance.save()
    context = {'breadcrumbs':breadcrumbs,}
    return render(request, 'assignment/instantiate.html', context)
