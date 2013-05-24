from django.template import Context, loader
from django.shortcuts import render
from django.contrib.auth.models import User
from assignment.models import *
from math import *
from random import shuffle


def detail(request, id):
    found = False
    #search for an already generated instance
    for q in QuestionInstance.objects.all():
        if q.template_id == int(id) and q.user_id == request.user.id:
            found = True
            question = q
            break
    #otherwise generate a question instance
    if not(found):
        template = Question.objects.get(pk=id)
        question = instanceQuestion(template, request.user)

    context = {
        'text': question.text,
        'answer': question.solution,
        'choices': question.choices.all(),
    }
    
    return render(request, 'question/instance.html', context)

def instanceQuestion(template, user):
    choices_list = template.choices.all()
    variables_list = template.variables.all()

    for v in variables_list:
        if not v.varType == 'custom':
            vars()[v.name] = v.getValue()

    template.solution = template.solution.replace('<br>', '\n')
    template.solution = template.solution.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
    exec template.solution
    solution = answer

    #question text formatted here
    variables = [] #init two-ple of variable names and values
    text = template.text
    for v in variables_list:
        variables.append(vars()[v.name])

    for v in variables_list:
        reg = '$'+v.name
        text = text.replace(reg, str(vars()[v.name]))

    #create question instance
    instance = QuestionInstance(title = template.title, solution=solution, text=text, user=user, template=template)
    instance.save()
    
    #choices formatted here
    if len(choices_list):
        for c in choices_list:
            c.solution = c.solution.replace('<br>', '\n')
            exec c.solution
            choice = Choice(solution=answer,question=instance)
            choice.save()
        #add solution to list of choices, shuffle choices
        choice = Choice(solution=solution,question=instance)
        choice.save()
        shuffle(instance.choices.all())
    
    return instance
