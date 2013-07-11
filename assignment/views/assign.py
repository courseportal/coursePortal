from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.contrib.auth.models import User
from django.utils import simplejson as json
from random import *
import string
from web.models import Class
from assignment.models import *
from math import *

def main(request):
    assignment_list = request.user.assignmentInstances.all()
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
    context = {'assignment_list': assignment_list, 'user': request.user, 'breadcrumbs':breadcrumbs}

    return render(request, 'assignment_nav.html', context)

def index(request):
    assignment_list = Assignment.objects.filter(private=False) | request.user.owned_assignments.all()
    context = {'user':request.user, 'assignment_list':assignment_list}

    return render(request, 'assignment/index.html', context)

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
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('assign'), 'title':'Assign'})
    context = {
        'users': User.objects.all(),
        'breadcrumbs': breadcrumbs,
        'assignments': request.user.owned_assignments.all(),
        'class_list': request.user.allowed_classes.all() | request.user.classes_authored.all()
    }
    return render(request, 'assignment/assign.html', context)

def instantiate(request):
    assignment = Assignment.objects.get(pk=request.POST['assignment'])
    #get list of users
    users=[]
    try:
        for u in User.objects.all().filter(pk=request.POST['users']):
            if users.count(u.id)==0:
                users.append(u)
    except:
        pass
    try:
        for c in Class.objects.all().filter(pk=request.POST['class']):
            for u in c.students.all():
                if users.count(u.id)==0:
                    users.append(u)
    except:
        pass

    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    data=json.loads(assignment.data)
    for u in users:
        instance=AssignmentInstance(title=assignment.title, user=u, template=assignment, start_date=assignment.start_date, due_date=assignment.due_date)
        instance.save()
        for question in assignment.questions.all():
            q=question.data
            q=json.loads(q)
            q['solution']= q['solution'].replace('<br>', '\n')
            q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            for integer_index in range(len(q['choices'])):
                q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
                q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
            exec q['code']
            solution=eval(q['solution'])
            #q text formatted here
            text = q['text']

            local_dict = dict(locals())
            text = string.Template(text).substitute(local_dict)
            question_instance = QuestionInstance(title=question.title, solution=solution, text=text, value=float(data['questions'][str(question.id)]), assignmentInstance=instance)
            question_instance.save()

            for choice in q['choices']:
                answer = eval(choice)
                choice_instance = ChoiceInstance(solution=answer, question=question_instance)
                choice_instance.save()
            if len(q['choices']) > 0:
                choice_instance = ChoiceInstance(solution=solution, question=question_instance)
                choice_instance.save()
            instance.max_score+=question_instance.value
            instance.save()
    context = {'breadcrumbs':breadcrumbs, 'messages':["Assignment succesfully assigned!"]}
    return render(request, 'assignment_nav.html', context)

def addA(request):
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('add_assignment'), 'title':'Add Assignment'})
    context = {
        'breadcrumbs':breadcrumbs,
        'question_list':request.user.owned_questions.all() | Question.objects.filter(private=False),
        'template_list':Template.objects.all(),
    }
    return render(request, 'assignment/addAssignment.html', context)

def editA(request, id):
    assignment = Assignment.objects.get(pk=id)
    assign_data = json.loads(assignment.data)
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('edit_assignment', args=[assignment.id]), 'title':'Edit Assignment'})
    context = {
        'assignment': assignment,
        'question_list':Question.objects.all(),
        'template_list':Template.objects.all(),
        'assign_data': assign_data,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'assignment/addAssignment.html', context)

def create(request):
    a=json.loads(request.POST['assignmentdata'])
    #Search for assignment by same name, delete it if found
    current=''
    try:
        current=request.user.owned_assignments.get(title = a['title'])
    except:
        pass
    if current!='':
        for q in current.questions.all():
            q.delete();
    #create new assignment
    assignment = Assignment(title = a["title"],due_date = a['due'],start_date = a['start'], data='')
    if 'private' in a:
        assignment.private = True
    assignment.save()

    data=dict()
    questions=dict()

    #save owners
    if current!='': 
        for x in current.owners.all():
            assignment.owners.add(x)
        current.delete();
    else:
        assignment.owners.add(request.user)

    #Add questions
    for q in a['questions']:
        temp=createQ(q, assignment.private, assignment.owners)
        assignment.questions.add(temp)
        questions[str(temp)]=q['points']
    data['questions']=questions
    #Finish
    assignment.data=json.dumps(data)
    assignment.save()
    return main(request)

def unassign(request):
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('unassign'), 'title':'Assign'})
    context = {
        'user': request.user,
        'breadcrumbs': breadcrumbs,
        'assignments': request.user.owned_assignments.all(),
        'class_list': request.user.allowed_classes.all() | request.user.classes_authored.all()
    }
    return render(request, 'assignment/unassign.html', context)

def unmake(request):
    try:
        instances = request.POST
        for i in instances:
            if i=="csrfmiddlewaretoken":
                continue
            instance = AssignmentInstance.objects.get(id=request.POST[i])
            for q in instance.questions.all():
                for c in q.choiceInstances.all():
                    c.delete()
                q.delete()
            instance.delete()
    except:
        pass
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    context = {'breadcrumbs':breadcrumbs, 'messages':["Assignment(s) succesfully unassigned!"]}
    return render(request, 'assignment_nav.html', context)

def createQ(x, private, users=[]):
    question = Question()
    question.private = private
    question.title = x['title']
    data=dict()
    question.data = json.dumps(x)
    question.save()
    for user in users.all():
        question.owners.add(user)
    question.save()
    return question.id