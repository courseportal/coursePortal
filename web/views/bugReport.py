from django.contrib import messages
#from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
import json
from web.forms.submission import bugReportForm
from web.models import AtomCategory, Submission, Class, BaseCategory, BugReport
from django.core.mail import send_mail, BadHeaderError


class PlainErrorList(ErrorList):
    """
    Look at this amazing class documentation
    
    """
    def __unicode__(self):
        """This function returns the unicode name of the class"""
        return self.as_plain()
    def as_plain(self):
        """This function returns the error message
        
        **Not sure**
        
        """
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])


#@login_required()
def index(request,bid):
    """
    Bug Report from Everyone 
    
    """
    if request.method == 'POST':
        form = bugReportForm(request.POST, error_class=PlainErrorList)
        if bid:
            if form.is_valid():
                b = BugReport.objects.get(pk=bid)
                b.subject = form.cleaned_data['subject']
                b.content = form.cleaned_data['content']
                b.email = form.cleaned_data['email']
                b.cc_myself = form.cleaned_data['cc_myself']
                b.save()
                messages.success(request, 'Successfully sent out, thanks!!! ')
                return HttpResponseRedirect(reverse('bugReport', args=[bid]))
            messages.warning(request, 'Error submitting. Fields might be invalid.')
        else:
            if form.is_valid():
                b = BugReport()
                b.subject = form.cleaned_data['subject']
                b.content = form.cleaned_data['content']
                b.email = form.cleaned_data['email']
                b.cc_myself = form.cleaned_data['cc_myself']
                b.save()
                subject = "[Bug Report]:  " + form.cleaned_data['subject']
                content = "From \"" + form.cleaned_data['email'] + "\" : \n\nBug Report:\n" + form.cleaned_data['content']

                if form.cleaned_data['cc_myself']:
                    try:
                        send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com','tyan@umich.edu'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                else:
                    try:
                        send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                return HttpResponseRedirect(reverse('bugReportConfirm', args=[b.id]))
            messages.warning(request, 'Error submitting.')
    else:
        form = bugReportForm()

    t = loader.get_template('web/home/bugReport.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'form': form,
    })
    return HttpResponse(t.render(c))

