from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render
from assignment.models import *
from web.models import *
from django.contrib.auth.models import User
from math import *
from random import *
import string, signal, sys

def matchType(request):
	vartype = request.GET['vartype']
	variable = Variable.objects.get(name=vartype)
	names = []
	for word in variable.variables.split('\n'):
		curVar={
			'name':word.split(',')[0],
			'defValue':word.split(',')[2]
		}
		names.append(curVar)
	return HttpResponse(json.dumps(names))

def getTypeCode(request):
	vartype = request.GET['vartype']
	variable = Variable.objects.get(name=vartype)
	return HttpResponse(json.dumps(variable.generated_code))

def timehandler(signum, frame):
	raise IOError("Program runs too long, possibly indicating an infinite loop!")

def validate(request):
	user_input = json.loads(request.GET['input'])
	vartype=Variable.objects.get(name=request.GET['vartype'])
	for x in range(0,len(vartype.variables.split('\n'))):
		variable_args = vartype.variables.split('\n')[x].split(',')
		locals()[variable_args[0]]=user_input[x]
		#Test that value can be of the correct type
		tryString = variable_args[1]+"("+locals()[variable_args[0]]+")"
		try:
			locals()[variable_args[0]] = eval(tryString)
		except:
			result = "Variable '"+str(variable_args[0])+"' needs to be of type "+variable_args[1]
			return HttpResponse(result)
	exec vartype.validation_code
	return HttpResponse(result)

def validateFull(request):
	#Limit runtime, feature only useable in unix environment
	if not sys.platform.startswith('win'):
		signal.signal(signal.SIGALRM, timehandler)
		signal.alarm(3) #will signal SIGALRM in 5 seconds
	try:
		exec request.GET['code']
	except MemoryError:
		return HttpResponse("Your code consumed too much memory, look for any non-terminating loops.")
	except Exception as e:
		return HttpResponse("Full Code did not validate! Here is the eror messages produced:\n" + str(e))
	return HttpResponse(0)

def practiceEval(request):
	question = Question.objects.get(id=request.GET['qid']) 
	if request.GET['status'] == True:
		question.numCorrect += 1
		question.save()
	else:
		question.numIncorrect += 1
		question.save()
	return HttpResponse("stuff")

def reportQ(request):
	question = Question.objects.get(id=request.GET['id'])
	subject = "Question Reported"
	message = "Your question '"+question.title+"' has been reported as broken. Here is the message submitted by a student:\n"
	message+= request.GET['text']
	send_mail(subject, message, 'test-no-use@umich.edu', [question.owners.all()[0].email])
	return HttpResponse('Success')
	
