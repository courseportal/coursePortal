from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render
from assignment.models import *
from web.models import Atom
from django.utils import simplejson as json
from random import *
from math import *
from string import Template
from knoatom.view_functions import get_breadcrumbs	
import sys

def detail(request, id, practice=False):
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
	if len(choices) > 0:
		try:
			choices.append(eval(solution))
		except Exception as ex:
			choices.append(solution)
	shuffle(choices)

	if not test=='':
		return HttpResponse(test)

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}
	if practice:
		return context
	return render(request, 'question/detail.html', context)

def addQ(request):
	context = get_breadcrumbs(request.path)
	context['type_list']= Variable.objects.all()
	context['atom_list']= Atom.objects.all()
	return render(request, 'question/addQ.html', context)

def create(request):
	q=''
	if 'qid' in request.POST:
		q = Question.objects.get(id=request.POST['qid'])
		q.owners.clear()
		q.atoms.clear()
		if q.copy.all()[0].owners.count() == 0:
			q.copy.all()[0].delete()
		else:
			q.copy.all()[0].original = None
			q.copy.all()[0].save()
	else:
		q = Question()
	q.title = request.POST['question_title']
	data=dict()
	data['code'] = request.POST['code']
	if data['code'][0] == '\r':
		data['code']=data['code'][2:]
	data['solution'] = request.POST['answer']
	data['text'] = request.POST['text']
	data['question_type'] = request.POST['question_type']
	choices = json.loads(request.POST['choices'])
	if data['question_type'] == 'True/False':
		if data['solution'] == 'True':
			choices.append('False')
		else:
			choices.append('True')
	data['choices']=json.dumps(choices)
	q.data=json.dumps(data)
	q.original = None
	q.save()
	q.owners.add(request.user)
	for atom in json.loads(request.POST['atoms']):
		q.atoms.add(Atom.objects.get(id=atom))
	#create copy
	q2 = Question()
	q2.title = q.title
	q2.data = q.data
	q2.isCopy = True
	q2.original = q
	q2.save()
	for atom in q.atoms.all():
		q2.atoms.add(atom)
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

def editQlist(request):
	context = get_breadcrumbs(request.path)
	context['question_list'] = request.user.owned_questions.filter(isCopy=False)
	return render(request, 'question/list.html', context)


