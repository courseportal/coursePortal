from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
from math import *
from random import *
import string


def checkAssignmentTitle(request):
	user = request.user
	title = request.POST['title']
	value = False
	overwrite=dict()
	try:
		if user.owned_assignments.filter(title=title):
			value = True
	except:
		pass
	overwrite['overwrite'] = value
	return HttpResponse(json.dumps(overwrite))

def replaceX(data):
	replace1="<input type=\"text\" name=\""
	replace2="\" class=\"t_input\" style='max-width:200px;' placeholder='"
	replace3="'></input>"
	toReplace=""
	while string.find(data, "@")>=0:
		toReplace=""
		index=string.find(data, "@")+1
		while index<len(data) and data[index] in string.ascii_letters+string.digits+"_":
			toReplace+=data[index]
			index=index+1
		data=string.replace(data, "@"+toReplace, replace1+toReplace+replace2+toReplace+replace3)
	return data

def test(request):
	context = {
		'type_list': Variable.objects.all(),
	}
	return render(request, 'assignment/test.html', context)

def matchType(request):
	vartype = request.GET['vartype']
	variable = Variable.objects.get(name=vartype)
	names = []
	for word in variable.variables.split():
		names.append(word)
	return HttpResponse(json.dumps(names))

def getTypeCode(request):
	vartype = request.GET['vartype']
	variable = Variable.objects.get(name=vartype)
	return HttpResponse(json.dumps(variable.generated_code))

def validate(request):
	user_input = json.loads(request.GET['input'])
	vartype=Variable.objects.get(name=request.GET['vartype'])
	
	for x in range(0,len(vartype.variables.split())):
		locals()[vartype.variables.split()[x]]=user_input[x]
	exec vartype.validation_code
	return HttpResponse(result)