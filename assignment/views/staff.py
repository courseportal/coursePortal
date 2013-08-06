from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
import numpy as np
from string import Template
from knoatom.view_functions import get_breadcrumbs
from math import *
from random import *

def viewStudent(request):
	user = request.user
	context = get_breadcrumbs(request.path)
	context['class_list']=user.classes_authored.all() | user.allowed_classes.all()
	context['user']=user
	return render(request, 'assignment/students.html', context)

def previewQuestion(request):
	q = json.loads(request.POST['questiondata'])

	preview = dict()
	preview['text'] = ''

	q['solution']= q['solution'].replace('<br>', '\n')
	q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	
	try: 
		exec q['code']
		preview['soln'] = eval(q['solution'])
		local_dict = dict(locals())
		preview['text'] = Template(q['text']).substitute(local_dict)

	except Exception as ex:
		preview['text'] += str(ex)

	return HttpResponse(json.dumps(preview))

def previewAssignment(request):
	assignment = json.loads(request.POST['previewdata'])
	question_list=[]
	test = ''
	for question in assignment['questions']:
		
		q=Question.objects.get(id=question)

		data = json.loads(q.data)
		data['solution']= data['solution'].replace('<br>', '\n')
		data['solution']= data['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')

		try:
			exec data['code']
		except Exception as ex:
			test += errorMsg(data['title'], ex, 'code')

		try:
			data['solution']=eval(data['solution'])
		except Exception as ex:
			test += errorMsg(data['title'], ex, 'solution')

		#q text formatted here
		local_dict = dict(locals())
		data['text'] = Template(data['text']).safe_substitute(local_dict)
		

		#format choices
		choices = json.loads(data['choices'])
		data['choices'] = []
		for choice in choices:
			try:
				answer = eval(choice)
				data['choices'].append(answer)
			except Exception as ex:
				y = "Choice"+str(integer_index+1)
				test += errorMsg(q.data['title'], ex, y)
		if len(data['choices']) > 0:
			data['choices'].append(data['solution'])

		data['title']=q.title
		question_list.append(data)

	if test!='':
		return HttpResponse(test)

	context = get_breadcrumbs(request.path)
	context['question_list']=question_list
	context['assignment']=assignment
	return render(request, 'assignment/preview.html', context)

def previewTemplate(request, a):
	assignment = Assignment.objects.get(pk=a)
	question_list=[]
	data = json.loads(assignment.data)
	for question in data:
		qdat = {
			'title': '',
			'text':'',
			'choices': '',
		}
		qdat['title'] = question['title']
		q=Question.objects.get(id=question['id']).data
		q=json.loads(q)
		q['choices']=json.loads(q['choices'])
		exec q['code']
		solution=eval(q['solution'])
		#q text formatted here
		local_dict = dict(locals())
		qdat['text'] = Template(q['text']).substitute(local_dict)

		qdat['choices'] = []
		for choice in q['choices']:
			answer = eval(choice)
			qdat['choices'].append(answer)
		if len(q['choices']) > 0:
			qdat['choices'].append(solution)
		shuffle(qdat['choices'])
		question_list.append(qdat)

	context = get_breadcrumbs(request.path)
	context['question_list']=question_list
	context['assignment']=assignment
	return render(request, 'assignment/preview.html', context)

def errorMsg(title, error, element):
	x = "Question \""+title+"\" threw this error in element \""+element+"\":<br>"
	x+= "&nbsp;&nbsp;&nbsp;&nbsp;"+str(error)+"<br>"
	return x

class AssignmentStats():
	assignmentName=''
	assignmentid=''
	data=[]
	average=0.0
	deviation=0.0
	minimum=0.0
	maximum=0.0
	median = 0.0
	numinstances = 0

def metrics(request):
	user=request.user
	stat_set=[]
	maxPossible=0
	achieved=0
	for a in user.owned_assignments.all():
		stats=AssignmentStats();
		stats.assignmentName=a.title
		stats.assignmentid=a.id
		#Generate data
		data=[]
		for i in a.instances.all():
			maxPossible = i.max_score
			achieved = i.score
			stats.numinstances += 1
			if maxPossible>0:
				data.append((achieved/maxPossible)*100)
		stats.data=data
		if(stats.numinstances > 0):
			#Calculate average
			stats.average = np.average(stats.data)#can add weighting
			#Calculate std deviation
			stats.deviation = np.std(stats.data)
			#Number completed?
			#Min, Max
			stats.minimum=np.amin(stats.data)
			stats.maximum=np.amax(stats.data)
			#median
			stats.median=np.median(stats.data)
		stat_set.append(stats)

	context = get_breadcrumbs(request.path)
	context["user"]=request.user
	context["stat_set"]=stat_set
	return render(request, 'assignment/metrics.html', context)

def deleteA(request):
	#Delete specified assignment
	if request.method == "POST":
		for entry in request.POST:
			if entry =="csrfmiddlewaretoken":
				continue
			assignment = Assignment.objects.get(id=entry)
			for question in assignment.questions.all():
				#See if we need to remove ownership from a copy
				if question.isCopy:
					removeOwner = True
					for a in request.user.owned_assignments.all():
						if a.id != assignment.id and a.questions.filter(id=question.id).exists():
							removeOwner=False
							break
					#remove ownership of copy, see if copy should be deleted
					if removeOwner:
						question.owners.remove(request.owner)
						#Copy has no owners and original has been changed
						if question.owners.all.count() == 0 and question.original == None:
							question.delete()

			assignment.delete() #deletes assigned instances as well

	context = get_breadcrumbs(request.path)
	context['assignment_list'] = request.user.owned_assignments.all()
	if request.method == "POST":
		context['messages']=['Assignment(s) deleted']
	return render(request, 'assignment/delete.html', context)

def deleteQ(request):
	#Delete specified questions
	if request.method == "POST":
		for entry in request.POST:
			if entry =="csrfmiddlewaretoken":
				continue
			question = Question.objects.get(id=entry)
			#Delete data entries in assignments
			for a in question.assigned_to.all():
				data = json.loads(a.data)
				for q in data:
					if int(q['id']) == int(question.id):
						data.remove(q)
				a.data = json.dumps(data)
				a.save()
			copy = question.copy.all()[0]
			if not copy.owners.all().exists():
				copy.delete()
			else:
				copy.original = None
				copy.save()
			question.delete()
			
	context = get_breadcrumbs(request.path)
	context['question_list'] = request.user.owned_questions.filter(isCopy=False)
	if request.method == "POST":
		context['messages'] = ['Question(s) deleted']
	return render(request, 'question/delete.html', context)

def selectInstance(request, messages=[]):
	context = get_breadcrumbs(request.path)
	context['assignments']=request.user.owned_assignments.all()
	context['messages']=messages
	return render(request, 'assignment/select.html', context)

def extend(request):
	try:
		date=request.POST['duedate']
		inputs = request.POST
		for i in inputs:
			if i=="csrfmiddlewaretoken" or i=="dudate":
				continue
			instance = AssignmentInstance.objects.get(id=request.POST[i])
			instance.due_date=date
			instance.save()
	except:
		pass
	messages=["Due dates extended"]
	return selectInstance(request, messages)