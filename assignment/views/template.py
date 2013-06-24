from django.http import HttpResponse
from django.template import Context, loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from assignment.models import *
from django.utils import simplejson as json
from random import *
from math import *

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