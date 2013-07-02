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
		if user.templates.filter(title=title):
			value=True
	except:
		pass
	overwrite['overwrite'] = value
	return HttpResponse(json.dumps(overwrite))

def replaceX(data):
	replace1="<input type=\"text\" name=\""
	replace2="\" class=\"t_input\"></input>"
	toReplace=""
	while string.find(data, "@")>=0:
		toReplace=""
		index=string.find(data, "@")+1
		while index<len(data) and data[index] in string.ascii_letters+string.digits+"_":
			toReplace+=data[index]
			index=index+1
		data=string.replace(data, "@"+toReplace, replace1+toReplace+replace2)
	return data