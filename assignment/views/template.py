from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *
import string

def addT(request):
	context= {
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

def detail(request,id):
	t=Template.objects.get(pk=id)
	data = json.loads(t.data)
	replace1="<input type=\"text\" name=\""
	replace2="\" class=\"t_input\"></input>"
	toReplace=""
	index=0
	#Go through text, replace @ with "<input type="text" name=" + characters + "></input>"
	while string.find(data['text'], "@")>=0:
		toReplace=""
		index=string.find(data['text'], "@")+1
		while data['text'][index] in string.ascii_letters+string.digits+"_":
			toReplace+=data['text'][index]
			index=index+1
		data['text']=string.replace(data['text'], "@"+toReplace, replace1+toReplace+replace2)

	#go through code, replace @ with "<input type="text" name=" + characters + "></input>"
	#replace "\n" with "<br>"
	data['code'] = string.replace(data['code'], "\n","<br>")
	while string.find(data['code'], "@")>=0:
		toReplace=""
		index=string.find(data['code'], "@")+1
		while data['code'][index] in string.ascii_letters+string.digits+"_":
			toReplace+=data['code'][index]
			index=index+1
		data['code']=string.replace(data['code'], "@"+toReplace, replace1+toReplace+replace2)

	context={
		'user':request.user,
		'data':data,
		'template':t,
	}
	return render(request, 'template/view.html', context)
