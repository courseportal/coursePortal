from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.template import Context, loader
from knoatom.view_functions import get_breadcrumbs  
from django.shortcuts import render, get_object_or_404
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
    assignment_list = Assignment.objects.all()
    context = {'user':request.user, 'assignment_list':assignment_list}

    return render(request, 'assignment/index.html', context)

def detail(request, id):
    assignment = get_object_or_404(AssignmentInstance, pk=id)
    #check if assignment was published
    if not assignment.was_published():
        return Http404
    #check if assignment was due
    if assignment.was_due():
        assignment.can_edit=False
        assignment.save()
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

def assign(request, messages=[]):
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('assign'), 'title':'Assign'})
    context = {
        'users': User.objects.all(),
        'breadcrumbs': breadcrumbs,
        'assignments': request.user.owned_assignments.all(),
        'class_list': request.user.allowed_classes.all() | request.user.classes_authored.all(),
        'messages':messages
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
            q['choices']=json.loads(q['choices'])
            exec q['code']
            solution=eval(q['solution'])
            #q text formatted here
            text = q['text']

            local_dict = dict(locals())
            text = string.Template(text).substitute(local_dict)
            question_instance = QuestionInstance(title=question.title, solution=solution, text=text, value=float(data['questions'][str(question.id)]), assignmentInstance=instance, template=question)
            question_instance.save()

            choices = []
            for choice in q['choices']:
                answer = eval(choice)
                choices.append(answer)
            if len(q['choices']) > 0:
                choices.append(solution)
            shuffle(choices)
            for choice in choices:
                choice_instance = ChoiceInstance(solution = choice, question=question_instance)
                choice_instance.save()
            instance.max_score+=question_instance.value
            instance.save()
    messages=["Assignment succesfully assigned!"]
    return assign(request, messages)

def addA(request):
    breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
    breadcrumbs.append({'url':reverse('add_assignment'), 'title':'Add Assignment'})
    context = {
        'isCopy':False,
        'breadcrumbs':breadcrumbs,
        'question_list':Question.objects.filter(isCopy=False),
    }
    return render(request, 'assignment/addAssignment.html', context)

def editA(request, id):
    assignment = Assignment.objects.get(pk=id)
    assign_data = json.loads(assignment.data)
    context = get_breadcrumbs(request.path)
    if assignment.owners.filter(id=request.user.id).exists():
        context['isCopy'] = False
    else:
        context['isCopy'] = True
    context['assignment']= assignment
    context['question_list']=Question.objects.filter(isCopy=False)
    context['assign_data']= assign_data
    return render(request, 'assignment/addAssignment.html', context)

def create(request):
    a=json.loads(request.POST['assignmentdata'])
    #Search for assignment by same name, delete it if found
    isCopy = request.POST['copystatus']
    current=''
    if isCopy == False:
        try:
            current=request.user.owned_assignments.get(title = a['title'])
        except:
            pass
    #create new assignment
    assignment = Assignment(title = a["title"],due_date = a['due'],start_date = a['start'], data='')
    if isCopy:
        assignment.isCopy = True;
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
        question = Question.objects.get(id=q['id'])
        #If user owns question, simply add it
        if question.owners.filter(id = request.user.id).exists():
            assignment.questions.add(question)
            questions[str(q['id'])]=q['points']
        #otherwise add copy, give user ownersip of copy
        else:
            if question.isCopy == False:
                question = question.copy #Retrieves copy
            questions[str(question.id)]=q['points']
            #Give ownership of copy if necessary
            if question.owners.filter(id = request.user.id).exists():
                question.owners.add(request.user)
                question.save()
    data['questions']=questions
    #Finish
    assignment.data=json.dumps(data)
    assignment.save()
    return main(request)

def unassign(request, messages=[]):
    context = get_breadcrumbs(request.path)
    context['user']= request.user,
    context['assignments']= request.user.owned_assignments.all(),
    context['class_list']= request.user.allowed_classes.all() | request.user.classes_authored.all(),
    context['messages']=messages
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
    messages=["Assignment(s) succesfully unassigned!"]
    return unassign(request, messages)
