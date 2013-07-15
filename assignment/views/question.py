from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *
from string import Template
from knoatom.view_functions import get_breadcrumbs	
import sys

def detail(request, id, newly_added=False):
	return HttpResponse("This needs to be written if you want to use it!")

def addQ(request):
	context = get_breadcrumbs(request.path)
	return render(request, 'question/addQ.html', context)

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

def preview(request):
	q = request.POST['previewdata']
	q = json.loads(q)
	test = ''
	try:
		exec q['code']
	except Exception as ex:
		test += "Error in code section:<br>"+str(ex)
		return HttpResponse(test)

	try:
		q['solution']= q['solution'].replace('<br>', '\n')
		q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
		for integer_index in range(len(q['choices'])):
			q['choices'][integer_index] = q['choices'][integer_index].replace('<br>', '\n')
			q['choices'][integer_index] = q['choices'][integer_index].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
		exec q['code']
		solution = eval(q['solution'])
	except Exception as ex:
		test += "Error in solutions:<br>"+str(ex)
		return HttpResponse(test)

	text = q['text']
	local_dict = dict(locals())
	text = Template(text).safe_substitute(local_dict)

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
