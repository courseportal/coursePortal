from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, get_object_or_404
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
import numpy as np
from string import Template
from knoatom.view_functions import get_breadcrumbs
from math import *
from random import *
import web.models, csv, StringIO

def viewStudent(request, id):
	selected_class = web.models.Class.objects.get(id=id) 
	user = request.user
	context = get_breadcrumbs(request.path)
	context['user_list']=selected_class
	context['user']=user
	context['class']=selected_class
	return render(request, 'assignment/students.html', context)

def previewQuestion(request):
	q = json.loads(request.POST['questiondata'])

	preview = dict()
	preview['text'] = ''

	q['solution']= q['solution'].replace('<br>', '\n')
	q['solution']= q['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')
	
	try: 
		exec q['code']
		preview['soln'] = eval(q['solution'])
		local_dict = dict(locals())
		preview['text'] = Template(q['text']).substitute(local_dict)

	except Exception as ex:
		preview['text'] += str(ex)

	return HttpResponse(json.dumps(preview))

def previewAssignment(request):
	assignment = json.loads(request.POST['previewdata'])
	question_list=[]
	for entry in assignment['questions']:
		
		question=Question.objects.get(id=entry)

		data = json.loads(question.data)
		data['text'] = question.text
		data['solution']= data['solution'].replace('<br>', '\n')
		data['solution']= data['solution'].replace('&nbsp;&nbsp;&nbsp;&nbsp;', '\t')

		exec question.code

		try:
			data['solution']=eval(data['solution'])
		except Exception as ex:
			pass

		#q text formatted here
		local_dict = dict(locals())
		data['text'] = Template(data['text']).safe_substitute(local_dict)
		

		#format choices
		choices = json.loads(data['choices'])
		data['choices'] = []
		for choice in choices:
			try:
				answer = eval(choice)
			except:
				answer=choice
			data['choices'].append(answer)
		if len(data['choices']) > 0:
			data['choices'].append(data['solution'])

		data['title']=question.title
		question_list.append(data)

	context = get_breadcrumbs(request.path)
	context['question_list']=question_list
	context['assignment']=assignment
	return render(request, 'assignment/preview.html', context)

def previewTemplate(request, a):
	assignment = Assignment.objects.get(pk=a)
	question_list=[]
	data = json.loads(assignment.data)
	for entry in data:
		qdat = {
			'title': '',
			'text':'',
			'choices': '',
		}
		qdat['title'] = entry['title']
		question=Question.objects.get(id=entry['id'])
		q=json.loads(question.data)
		q['choices']=json.loads(q['choices'])
		exec question.code
		solution=eval(q['solution'])
		#q text formatted here
		local_dict = dict(locals())
		qdat['text'] = Template(question.text).substitute(local_dict)

		qdat['choices'] = []
		for choice in q['choices']:
			answer = eval(choice)
			qdat['choices'].append(answer)
		if len(q['choices']) > 0:
			qdat['choices'].append(solution)
		shuffle(qdat['choices'])
		question_list.append(qdat)

	context = get_breadcrumbs(request.path)
	context['question_list']=question_list
	context['assignment']=assignment
	return render(request, 'assignment/preview.html', context)

class AssignmentStats():
	assignmentName=''
	assignmentid=''
	data=[]
	average=0.0
	deviation=0.0
	minimum=0.0
	maximum=0.0
	median = 0.0
	numinstances = 0

def metrics(request):
	user=request.user
	stat_set=[]
	maxPossible=0
	achieved=0
	for a in user.owned_assignments.all():
		stats=AssignmentStats();
		stats.assignmentName=a.title
		stats.assignmentid=a.id
		#Generate data
		data=[]
		for i in a.instances.all():
			maxPossible = i.max_score
			achieved = i.score
			stats.numinstances += 1
			if maxPossible>0:
				data.append((achieved/maxPossible)*100)
		stats.data=data
		if(len(data)>0):
			#Calculate average
			stats.average = np.average(stats.data)#can add weighting
			#Calculate std deviation
			stats.deviation = np.std(stats.data)
			#Number completed?
			#Min, Max
			stats.minimum=np.amin(stats.data)
			stats.maximum=np.amax(stats.data)
			#median
			stats.median=np.median(stats.data)
		stat_set.append(stats)

	context = get_breadcrumbs(request.path)
	context["user"]=request.user
	context["stat_set"]=stat_set
	return render(request, 'assignment/metrics.html', context)

def deleteA(request, id):
	#Delete specified assignment
	try:
		assignment = Assignment.objects.get(id=id)
	except:
		return HttpResponse('Failure')
	for question in assignment.questions.all():
		#See if we need to remove ownership from a copy
		if question.isCopy:
			removeOwner = True
			for a in request.user.owned_assignments.all():
				if a.id != assignment.id and a.questions.filter(id=question.id).exists():
					removeOwner=False
					break
			#remove ownership of copy, see if copy should be deleted
			if removeOwner:
				question.owners.remove(request.owner)
				#Copy has no owners and original has been changed
				if question.owners.all.count() == 0 and question.original == None:
					question.delete()
	assignment.delete() #deletes assigned instances as well

	return HttpResponse('Success!')

def deleteQ(request, id):
	#Delete specified question
	try:
		question = Question.objects.get(id=id)
	except:
		return HttpResponse('Failure!')
	#Delete data entries in assignments
	for a in question.assigned_to.all():
		data = json.loads(a.data)
		while str(question.id) in json.dumps(data):
			for q in data:
				if int(q['id']) == int(question.id):
					data.remove(q)
		a.data = json.dumps(data)
		a.save()
	copy = question.copy.all()[0]
	if not copy.owners.all().exists():
		copy.delete()
	else:
		copy.original = None
		copy.save()
	question.delete()
			
	return HttpResponse('Success!')

def editQ(request, id):
	question = get_object_or_404(Question, id=id)
	#Generate list of variables
	variable_list = []
	varCode = question.code.split('#CUSTOM')[0].replace('\r\n', '\n')
	if varCode.find('#var:') >= 0:
		for content in varCode.split('#var')[1:]:
			variable={
				'vartype':'',
				'varname':'',
				'vardata':dict(),
			}
			variable['vartype'] = content.split('\n')[0].split('_')[0]
			variable['varname'] = content.split('\n')[0].split('_')[1]
			for line in content.split('#Template Code\n')[0].split('\n')[1:-1]:
				variable['vardata'][line.split('=')[0]] = line.split('=')[1]
			variable_list.append(variable)
	#Get code
	code = question.code.split('#CUSTOM')[1]

	context=get_breadcrumbs(request.path)
	context['qdata'] = json.loads(question.data)
	context['code'] = code
	context['text'] = question.text
	context['variable_list'] = variable_list
	context['question'] = question
	context['type_list'] = Variable.objects.all()
	context['atom_list'] = web.models.Atom.objects.all()
	return render(request, 'question/addQ.html', context)

def selectInstance(request, c, messages=[]):
	context = get_breadcrumbs(request.path)
	context['class'] = web.models.Class.objects.get(id=c)
	context['assignments']=request.user.owned_assignments.all()
	context['messages']=messages
	return render(request, 'assignment/select.html', context)

def extend(request):
	date=request.POST['duedate']
	inputs = request.POST
	for i in inputs:
		if i=="csrfmiddlewaretoken" or i=="duedate" or i=="classid":
			continue
		instance = AssignmentInstance.objects.get(id=request.POST[i])
		instance.due_date=date
		instance.save()
	messages=["Due dates extended"]
	return selectInstance(request, request.POST['classid'], messages)

def csvList(request, cid, messages=[]):
	context = get_breadcrumbs(request.path)
	context['class'] = web.models.Class.objects.get(id=cid)
	context['assignments']=request.user.owned_assignments.all()
	context['messages']=messages
	return render(request, 'assignment/selectCSV.html', context)

def emailCSV(request, cid, aid):
	c=web.models.Class.objects.get(id=cid)
	template = Assignment.objects.get(id=aid)
	csvfile=StringIO.StringIO()
	csvwriter =csv.writer(csvfile)
	#get instances to look at
	instance_list = c.assigned_instances.filter(template=template)

	if instance_list.count() == 0:
		return csvList(request, cid, ['No data to report on that assignment'])

	#go through each question of template
	question_list = json.loads(template.data)
	for x in range(0,len(question_list)):
		#add header row
		csvwriter.writerow(['uid', 'question', 'score.'+str(question_list[x]['points'])])
		#Go through each question instance
		for instance in instance_list:
			#add data row
			question = instance.questions.all()[x]
			if question.student_answer == question.solution:
				csvwriter.writerow([instance.user.email, question.title, question.value])
			else:
				csvwriter.writerow([instance.user.email, question.title, '0'])
		csvwriter.writerow([])

	#send email
	email = EmailMessage()
	email.subject = 'Cportal Class Data'
	email.body = 'Attached is the class data for '+c.title+" assignment "+template.title
	email.to = [request.user.email]
	email.attach(str(c.title)+'_'+template.title+'.csv', csvfile.getvalue(), 'text/csv')
	email.send()
	return render(request, 'assignment_nav.html')