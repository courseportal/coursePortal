from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from random import shuffle

def index(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
    context = {'assignment_list': assignment_list, 'user': request.user, 'breadcrumbs':breadcrumbs}

    return render(request, 'assignment/index.html', context)

def detail(request, id):
    assignment = request.user.assignmentInstances.get(pk=id)
    question_list = assignment.questions.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'assignment'}]
    breadcrumbs.append({'url': reverse('assignment_detail', args=[assignment.id]), 'title': assignment})
    context = {
        'assignment_list': request.user.assignmentInstances.all(),
        'assignment_selected': assignment,
        'question_list': question_list,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'assignment/detail.html', context)

def assign(request):
    user_list = User.objects.all()
    assignment_list = Assignment.objects.all()
    context = {
        'users': user_list,
        'assignments': assignment_list,
    }
    return render(request, 'assignment/assign.html', context)

def instantiate(request):
    assignment = Assignment.objects.get(pk=request.POST['assignment'])
    users = User.objects.all().filter(pk=request.POST['users'])

    for u in users:
        instance = AssignmentInstance(title=assignment.title, user=u, template=assignment)
        instance.save()
        for question in assignment.questions.all():
            choices_list = question.choices.all()
            variables_list = question.variables.all()

            for variable in variables_list:
                if not variable.varType == 'custom':
                    vars()[variable.name] = variable.getValue()

            question.solution = question.solution.replace('<br>', '\n')
            question.solution = question.solution.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            exec question.solution
            solution = answer

            #question text formatted here
            variables = [] #init two-ple of variable names and values
            text = question.text
            for variable in variables_list:
                variables.append(vars()[variable.name])

            for variable in variables_list:
                reg = '$'+variable.name
                text = text.replace(reg, str(vars()[variable.name]))

            #create question instance
            question_instance = QuestionInstance(title = question.title, solution=solution, text=text, assignmentInstance=instance, value=question.value)
            instance.max_score+=question_instance.value;
            question_instance.save()
            
            #choices formatted here
            if len(choices_list):
                for choice in choices_list:
                    choice.solution = choice.solution.replace('<br>', '\n')
                    exec choice.solution
                    choice_instance = ChoiceInstance(solution=answer,question=question_instance)
                    choice_instance.save()
                #add solution to list of choices, shuffle choices
                choice_instance = ChoiceInstance(solution=solution,question=question_instance)
                choice_instance.save()
            instance.save()

    return render(request, 'assignment/instantiate.html')


def grades(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'assignment'}]
    breadcrumbs.append({'url': reverse('grades'), 'title': 'grades'})
    context = {
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
        assignment.save();
    return index(request)