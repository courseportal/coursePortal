from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
import numpy as np
from string import Template
from math import *
from random import *

def viewStudent(request):
	user = request.user
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
	context = {
		'class_list': user.classes_authored.all() | user.allowed_classes.all(),
		'user': user,
		'breadcrumbs':breadcrumbs
	}
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

	context = {
		'question_list': question_list,
		'assignment': assignment
	}

	return render(request, 'assignment/preview.html', context)

def previewTemplate(request, a):
	assignment = Assignment.objects.get(pk=a)
	question_list=[]
	test = ''
	
	for q in assignment.questions.all():
		question={
			'title':'',
			'solution':'',
			'text':'',
			'choices':[]
	   }
		q=json.loads(q.data)
		question['title'] = q['title']
		q['solution']= q['solution'].replace('<br>', '\n')
		q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
		try:
			exec q['code']
		except Exception as ex:
			test += errorMsg(q['title'], ex, 'code')

		try:
			question['solution']=eval(q['solution'])
		except Exception as ex:
			test += errorMsg(q['title'], ex, 'solution')

		#Format chice texts
		for integer_index in range(len(q['choices'])):
			q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
			q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
			

		#q text formatted here
		local_dict = dict(locals())
		question['text'] = Template(q['text']).substitute(local_dict)

		for integer_index in range(len(q['choices'])):
			try:
				answer = eval(q['choices'][integer_index])
				question['choices'].append(answer)
			except Exception as ex:
				y = "Choice"+str(integer_index+1)
				test += errorMsg(q['title'], ex, y)
		if len(q['choices']) > 0:
			question['choices'].append(question['solution'])
		question_list.append(question)

	if test!='':
		return HttpResponse(test)
	context = {
		'question_list': question_list,
   		'assignment': assignment
	}
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

	context = {
		"user":request.user,
		"stat_set":stat_set,
	}
	return render(request, 'assignment/metrics.html', context)

def deleteA(request):
	#Delete specified assignment
	if request.method == "POST":
		for entry in request.POST:
			if entry =="csrfmiddlewaretoken":
				continue
			assignment = Assignment.objects.get(id=entry)
			assignment.delete()
			#delete assigned instances?
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	context = {
		'assignment_list': request.user.owned_assignments.all(),
		'breadcrumbs':breadcrumbs
	}
	if request.method == "POST":
		context['messages']=['Assignment(s) deleted']
	
	#breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
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
				try:
					data = json.loads(a.data)
					del data['questions'][str(question.id)]
					a.data = json.dumps(data)
				except:
					pass
				a.save()
			question.delete()
			#delete assigned instances?
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	context = {
		'question_list': Question.objects.all(),
		'breadcrumbs':breadcrumbs
	}
	if request.method == "POST":
		context['messages']=['Question(s) deleted']
	
	#breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
	return render(request, 'question/delete.html', context)

