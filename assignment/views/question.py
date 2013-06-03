from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *

def index(request):
	question_list = Question.objects.all()
	context = {'question_list': question_list}
	return render(request, 'question/index.html', context)

def detail(request, id):
	question = Question.objects.get(pk=id)
	choices_list = question.choices.all()
	variables_list = question.variables.all()

	for v in variables_list:
		if not v.varType == 'custom':
			vars()[v.name] = v.getValue()

	question.solution = question.solution.replace('<br>', '\n')
	question.solution = question.solution.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	exec question.solution
	solution = answer

	#question text formatted here
	variables = [] #init two-ple of variable names and values
	text = question.text
	for v in variables_list:
		variables.append(vars()[v.name])

	for v in variables_list:
		template = '$'+v.name
		text = text.replace(template, str(vars()[v.name]))

	#choices formatted here
	choices = []
	for c in choices_list:
		c.solution = c.solution.replace('<br>', '\n')
		exec c.solution
		choices.append(answer)

	context = {
		'text': text,
		'answer': solution,
		'choices': choices,
	}

	return render(request, 'question/question.html', context)

def test(request):
	return render(request, 'question/test.html')

def testindex(request):
	question_list = TestQuestion.objects.all()
	context = {'question_list': question_list}
	return render(request, 'question/testindex.html', context)

def testdetail(request, id):
	question = TestQuestion.objects.get(pk=id)
	q = json.loads(question.data)
	q['solutions'][0] = q['solutions'][0].replace('<br>', '\n')
	q['solutions'][0] = q['solutions'][0].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	exec q['solutions'][0]
	solution = answer

	#q text formatted here
	text = q['texts'][0]
	
	local_dict = dict(locals())
	for v in local_dict:
		replace = '$'+v
		text = text.replace(replace, str(locals()[v]))

	# #choices formatted here
	# choices = []
	# for c in choices_list:
	# 	c.solution = c.solution.replace('<br>', '\n')
	# 	exec c.solution
	# 	choices.append(answer)

	context = {
		'text': text,
		'answer': solution,
		# 'choices': choices,
	}

	return render(request, 'question/question.html', context)

def create(request):
	q = TestQuestion()
	q.name = request.REQUEST['questionname']
	q.data = request.REQUEST['questiondata']
	q.save()
	return HttpResponse(request.REQUEST['questiondata'])