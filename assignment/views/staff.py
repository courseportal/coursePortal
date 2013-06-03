from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User

def viewStudent(request):
	user = request.user
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
	context = {
   	'class_list': user.author.all(),
   	'user': user,
   	'breadcrumbs':breadcrumbs
   }
	return render(request, 'assignment/students.html', context)