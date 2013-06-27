from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *
import string
from assignment.views.utility import replaceX

def indexA(request):
	context = {
		'user':request.user,
		'template_list': ATemplate.objects.all(),
	}
	return render(request, 'template/index.html', context)

def indexQ(request):
	context = {
		'user':request.user,
		'template_list': Template.objects.all(),
	}

def addT(request):
	context = {
		'user':request.user,
	}
	return render(request, 'template/addT.html', context);

def create(request):
	t = Template()
	t.title = request.REQUEST['templatename']
	t.data = request.REQUEST['templatedata']
	t.save()
	# return HttpResponse(request.REQUEST['questiondata'])
	return render(request, 'assignment_nav.html')

def create_assignment(request):
	a=json.loads(request.POST['assignmentdata'])
	assignment = ATemplate(title = a["title"], data='')
	assignment.save()
   #save start and end date
	data=dict()
	data['due']=a['due']
	data['start']=a['start']
	questions=dict()
   #save owners
	assignment.owners.add(request.user)
   #Add questions
	for q in a['questions']:
		temp=createQT(q)
		assignment.questions.add(temp)
		questions[str(temp)]=q['points']
	data['questions']=questions
   #Finish
	assignment.data=json.dumps(data)
	assignment.save()
	return HttpResponse(assignment)

def createQT(x):
	question = Template()
	question.title = x['title']
	data=dict()
	data['title']=x['title']
	data['code']=x['code']
	data['text']=x['text']
	data['solution']=x['solution']
	data['choices']=x['choices']
	question.data = json.dumps(data)
	question.save()
	return question.id

def genQ(request):
	t = Template.objects.get(pk=request.POST["tid"])
	q = Question()
	q.title = t.title
	#replae @ symbols
	data = t.data
	#prepend assignment statements
	for key in request.POST.keys():
		if key=="tid" or key=="csrfmiddlewaretoken":
			continue
		data=string.replace(data, "@"+key, request.POST[key]);
	q.data = data
	q.save()
	return HttpResponse(q.data)

def genA(request):
	template = ATemplate.objects.get(pk=request.POST['tid'])
	data=dict()
	data["start"] = json.loads(template.data)['start']
	data["due"] =json.loads(template.data)['due']
	assignment = Assignment(title=template.title, data=json.dumps(data));
	assignment.save()
	assignment.owners.add(request.user)
	questions = list(template.questions.all());
	
	#Parse inputs
	for key in request.POST.keys():
		if key=="tid" or key=="csrfmiddlewaretoken":
			continue
		questions[int(key[0])-1].data = string.replace(questions[int(key[0])-1].data, "@"+key[1:], request.POST[key])

	#create questions
	for question in questions:
		q = Question(title = question.title, data=question.data)
		q.save();
		assignment.questions.add(q)
		data=json.loads(assignment.data)
		data[q.id]=0
		assignment.data=json.dumps(data)
	assignment.save()

	return HttpResponse(assignment.data)


def detailQ(request,id):
	t=Template.objects.get(pk=id)
	data = json.loads(t.data)
	#Go through text, replace @ with "<input type="text" name=" + characters + "></input>"
	data['text']=replaceX(data['text'])

	#go through code, replace @ with "<input type="text" name=" + characters + "></input>"
	data['code'] = string.replace(replaceX(data['code']), "\n","<br>")

	context={
		'user':request.user,
		'data':data,
		'template':t,
	}
	return render(request, 'template/view.html', context)

def detailA(request, id):
	t=ATemplate.objects.get(pk=id)
	question_list=[];

	for q in t.questions.all():
		data = json.loads(q.data)
		#Go through text, replace @ with "<input type="text" name=" + characters + "></input>"
		data['text']=replaceX(data['text'])
		#go through code, replace @ with "<input type="text" name=" + characters + "></input>"
		data['code'] = string.replace(replaceX(data['code']), "\n","<br>")
		question_list.append({'title':q.title, 'data':data})

	context={
		'user':request.user,
		'question_list':question_list,
		'template':t,
	}

	return render(request, 'template/viewA.html', context)
