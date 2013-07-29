from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from web.models import Atom
from django.utils import simplejson as json
from random import *
from math import *
from string import Template
from knoatom.view_functions import get_breadcrumbs	
import sys

def detail(request, id, newly_added=False):
	q=Question.objects.get(id=id)
	data=json.loads(q.data)
	test = ''
	try:
		exec data['code']

	except Exception as ex:
		test += "Error in code section:<br>"+str(ex)+"<br>"

	try:
		solution = eval(data['solution'])
	except:
		solution = data['solution']

	text = data['text']
	local_dict = dict(locals())
	text = Template(text).safe_substitute(local_dict)
	

	# #choices formatted here
	choices = []
	for choice in json.loads(data['choices']):
		choice = Template(choice).safe_substitute(local_dict)
		try:
			choices.append(eval(choice))
		except Exception as ex:
			choices.append(choice)

	if not test=='':
		return HttpResponse(test)

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}
	return render(request, 'question/detail.html', context)

def addQ(request):
	context = get_breadcrumbs(request.path)
	context['type_list']= Variable.objects.all()
	context['atom_list']= Atom.objects.all()
	return render(request, 'question/addQ.html', context)

def create2(request):
	q = Question()
	q.title = request.POST['question_title']
	data=dict()
	data['code'] = request.POST['code']
	data['solution'] = request.POST['answer']
	data['text'] = request.POST['text']
	choices = json.loads(request.POST['choices'])
	if request.POST['question_type'] == 'True/False':
		if data['solution'] == 'True':
			choices.append('False')
		else:
			choices.append('True')
	data['choices']=json.dumps(choices)
	q.data=json.dumps(data)
	q.save()
	q.owners.add(request.user)
	context = get_breadcrumbs(request.path)
	context['messages'] = ['Question sucessfully created']
	return render(request, "assignment_nav.html", context)

def preview(request):
	q=dict()
	q['code'] = request.POST['code']
	q['text'] = request.POST['text']
	q['solution'] = request.POST['answer']
	q['choices'] = json.loads(request.POST['choices'])
	test = ''
	try:
		exec q['code']

	except Exception as ex:
		test += "Error in code section:<br>"+str(ex)+"<br>"

	try:
		solution = eval(q['solution'])
	except Exception as ex:
		solution = q['solution']

	text = q['text']
	local_dict = dict(locals())
	text = Template(text).safe_substitute(local_dict)

	# #choices formatted here
	choices = []
	for choice in q['choices']:
		try:
			choices.append(eval(choice))
		except Exception as ex:
			choices.append(choice)

	if not test=='':
		return HttpResponse(test)

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}
	return render(request, 'question/preview.html', context)

def instanceDetail(request, pk, id):
	assignmentInstance = request.user.assignmentInstances.get(pk=pk)
	question = assignmentInstance.questions.get(pk=id)
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'assignment'}]
	breadcrumbs.append({'url': reverse('assignment_detail', args=[assignmentInstance.id]), 'title': assignmentInstance})
	breadcrumbs.append({'url': reverse('question_instance', args=[assignmentInstance.id, question.id]), 'title': question})
	context = {
		'user': request.user,
		'question_selected': question,
		'q':question,
    	'assignment_selected': assignmentInstance,
		'text': question.text,
		'choices': question.choiceInstances.all(),
		'breadcrumbs': breadcrumbs,
	}
    
	return render(request, 'question/instance.html', context)

def create(request):
	q = Question()
	q.title = request.REQUEST['questionname']
	q.data = request.REQUEST['questiondata']
	q.save()
	q.owners.add(request.user)
	q.save()
	context={
		'messages':["Question succesfully made!"],
	}
	return render(request, "assignment_nav.html", context)
