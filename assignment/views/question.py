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
	question=Question.objects.get(id=id)
	data=json.loads(question.data)
	test = ''
	try:
		exec question.code
	except Exception as ex:
		test += "Error in code section:<br>"+str(ex)+"<br>"

	try:
		solution = eval(data['solution'])
	except:
		solution = data['solution']

	text = question.text
	local_dict = dict(locals())
	text = Template(text).safe_substitute(local_dict)
	
	#choices formatted here
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

	context = get_breadcrumbs(request.path)
	context['text']=text
	context['answer']=solution
	context['choices']=choices
	if practice:
		return context
	return render(request, 'question/detail.html', context)

def addQ(request):
	context = get_breadcrumbs(request.path)
	context['type_list']= Variable.objects.all()
	context['atom_list']= Atom.objects.all()
	return render(request, 'question/addQ.html', context)

def create(request):
	#Create or get question
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

	#Set privacy
	if 'Make_Q_Private' in request.POST:
		q.is_private = True
	q.title = request.POST['question_title']
	data=dict()
	code = request.POST['code']
	if code[0] == '\r':
		code=code[2:]
	data['solution'] = request.POST['answer']
	data['question_type'] = request.POST['question_type']
	choices = json.loads(request.POST['choices'])
	if data['question_type'] == 'True/False':
		if data['solution'] == True:
			choices.append('False')
		else:
			choices.append('True')
	data['choices']=json.dumps(choices)
	q.data=json.dumps(data)
	q.code=code
	q.text=request.POST['text']
	q.original = None
	q.save()
	q.owners.add(request.user)
	for atom in json.loads(request.POST['atoms']):
		q.atoms.add(Atom.objects.get(id=atom))
	#create copy if not private
	if q.is_private == False:
		q2 = Question()
		q2.title = q.title
		q2.data = q.data
		q2.code = q.code
		q2.text = q.text
		q2.isCopy = True
		q2.original = q
		q2.save()
		for atom in q.atoms.all():
			q2.atoms.add(atom)
	return HttpResponse('Success!')

def preview(request):
	code = request.POST['code']
	text = request.POST['text']
	q=dict()
	q['solution'] = request.POST['answer']
	q['choices'] = json.loads(request.POST['choices'])
	try:
		exec code
	except Exception as ex:
		return HttpRespons("Error in code section:<br>"+str(ex)+"<br>")

	try:
		solution = eval(q['solution'])
	except Exception as ex:
		solution = q['solution']

	local_dict = dict(locals())
	text = Template(text).safe_substitute(local_dict)

	# #choices formatted here
	choices = []
	for choice in q['choices']:
		try:
			choices.append(eval(choice))
		except Exception as ex:
			choices.append(choice)

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}
	return render(request, 'question/preview.html', context)

def instanceDetail(request, pk, id):
	assignmentInstance = request.user.assignmentInstances.get(pk=pk)
	question = assignmentInstance.questions.get(pk=id)
	context = get_breadcrumbs(request.path)
	context['user']=request.user
	context['question_selected']=question
	context['q']=question
	context['assignment_selected']=assignmentInstance
	context['text']=question.text
	context['choices']=question.choiceInstances.all()
    
	return render(request, 'question/instance.html', context)

def Qlist(request):
	context = get_breadcrumbs(request.path)
	context['question_list'] = request.user.owned_questions.filter(isCopy=False)
	return render(request, 'question/list.html', context)


