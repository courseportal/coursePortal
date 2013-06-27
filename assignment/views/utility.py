from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
from math import *
from random import *
from string import find


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