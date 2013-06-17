from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
import numpy as np

def viewStudent(request):
	user = request.user
	breadcrumbs = [{'url': reverse('assignment'), 'title': 'Assignments'}]
	breadcrumbs.append({'url': reverse('view_student'), 'title': 'Students'})
	context = {
   	'class_list': user.author.all() | user.allowed_classes.all(),
   	'user': user,
   	'breadcrumbs':breadcrumbs
   }
	return render(request, 'assignment/students.html', context)

class ClassStats():
	className=''
	classid=''
	data=[]
	average=0.0
	deviation=0.0
	minimum=0.0
	maximum=0.0
	plot=None
	


def metrics(request):
	user=request.user
	stat_set=[]
	maxPossible=0
	achieved=0
	for c in user.allowed_classes.all() | user.author.all():
		stats=ClassStats();
		stats.className=c.name
		stats.classid=c.id
		#Generate data
		data=[]
		maxPossible = 0.0
		achieved = 0.0
		for s in c.students.all():
			for i in s.assignmentInstances.all():
				maxPossible+=i.max_score
				achieved+=i.score
			if maxPossible>0:
				data.append((achieved/maxPossible)*100)
		stats.data=data
		#Calculate average
		stats.average = np.average(stats.data)#can add weighting
		#Calculate std deviation
		stats.deviation = np.std(stats.data)
		#Number completed?
		#Min, Max
		stats.minimum=np.nanmin(stats.data)
		stats.maximum=np.nanmax(stats.data)
		#median
		stats.median=np.median(stats.data)
		stat_set.append(stats)

	context = {
		"user":request.user,
		"stat_set":stat_set,
	}
	return render(request, 'assignment/metrics.html', context)



	