import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render


from knoatom.forms import bugReportForm
from knoatom.models import BugReport

def bug_report_view(request):
	r"""
	This view handles the form for bug reports
	
	"""
	
	if request.method != 'POST': # If the form has been submitted...
		return HttpResponseNotAllowed(['POST'])
	form = bugReportForm(request.POST)
	if form.is_valid():	# All validation rules pass
		
		b = BugReport()
		b.subject = form.cleaned_data['subject']
		b.content = form.cleaned_data['content']
		b.email = form.cleaned_data['email']
		b.save()
		subject = "[Bug Report]:  " + form.cleaned_data['subject']
		content = "From \"" + form.cleaned_data['email'] + "\" : \n\nBug Report:\n" + form.cleaned_data['content']
		
		try:
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
		except BadHeaderError:
			return HttpResponse('Invalid header found.')

		data = json.dumps({'success':True, 'message': '<div class="alert alert-success">Successfully submitted bug report!</div>', 'html':render(request, 'web/form_template.html', {'form': bugReportForm()}).content})
		#return HttpResponse(context={'bugReportform':form})
		return HttpResponse(data, mimetype="application/json")	
	else:
		#data = json.dumps(dict([(k, [unicode(e) for e in v]) for k,v in form.errors.items()]).update({'message': 'Some fields are invalid!', 'success':False}))
		data = json.dumps({'html':render(request, 'web/form_template.html', {'form':form}).content})
		return HttpResponse(data, mimetype="application/json")	