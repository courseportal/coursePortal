from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *
from string import Template
import sys

def index(request):
	question_list = Question.objects.all()
	context = {'question_list': question_list}
	return render(request, 'question/index.html', context)

def detail(request, id, newly_added=False):
	question = Question.objects.get(pk=id)
	q = json.loads(question.data)

	test = ''
	try:
		exec q['code']
	except Exception as ex:
		test += str(ex)
		return HttpResponse(test)


	q['solution']= q['solution'].replace('<br>', '\n')
	q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	for integer_index in range(len(q['choices'])):
		q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
		q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	exec q['code']
	solution = eval(q['solution'])

	#q text formatted here
	text = q['text']
	# shuffle(q['texts'])
	# text = q['texts'][0]

	local_dict = dict(locals())
	text = Template(text).substitute(local_dict)

	# #choices formatted here
	choices = []
	for choice in q['choices']:
		choices.append(eval(choice))

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
		'newly_added': newly_added,
	}

	return render(request, 'question/question.html', context)

def addQ(request):
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignment'}]
	breadcrumbs.append({'url':reverse('add_question'), 'title':'Add Question'})
	context = {'breadcrumbs':breadcrumbs,}
	return render(request, 'question/addQ.html', context)

def create(request):
	q = Question()
	q.title = request.REQUEST['questionname']
	q.data = request.REQUEST['questiondata']
	q.save()
	# return HttpResponse(request.REQUEST['questiondata'])
	return detail(request, q.id, True)

def preview(request):
	q = request.POST['previewdata']
	q = json.loads(q)
	test = ''
	try:
		exec q['code']
	except Exception as ex:
		test += str(ex)
		return HttpResponse(test)

	q['solution']= q['solution'].replace('<br>', '\n')
	q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	for integer_index in range(len(q['choices'])):
		q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
		q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	exec q['code']
	solution = eval(q['solution'])

	#q text formatted here
	text = q['text']
	# shuffle(q['texts'])
	# text = q['texts'][0]

	local_dict = dict(locals())
	text = Template(text).substitute(local_dict)

	# #choices formatted here
	choices = []
	for choice in q['choices']:
		choices.append(eval(choice))

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}

	return render(request, 'question/preview.html', context)

def form(request):
	return render(request, 'question/form.html')


