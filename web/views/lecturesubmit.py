from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response
import json
from web.forms.submission import LectureNoteForm
from web.models import AtomCategory, LectureNote, Class
from knoatom.settings import MEDIA_ROOT



class PlainErrorList(ErrorList):
    def __unicode__(self):
        return self.as_plain()
    def as_plain(self):
        if not self: return u''
        return u'<br/>'.join([ e for e in self ])

def media_root():
    return MEDIA_ROOT

@login_required()
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required()
def index(request, pk):
    
    class_id = get_object_or_404(Class, pk=pk)
    
    if request.method == 'POST':
        form = LectureNoteForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            f = form.save(commit=False)
            f.classBelong = class_id
            f.owner = class_id.author
            f.filename = form.cleaned_data['filename']
            f.save()
    #        return HttpResponseRedirect('/success/LectureNoteUpload/')
    else:
        form = LectureNoteForm()
    t = loader.get_template('LectureNoteUpload.html')
    c = RequestContext(request, {
                   'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
                   'form': form,
                   'parent_categories': AtomCategory.objects.filter(parent=None),
                   'class_id': class_id,
                   })
    return HttpResponse(t.render(c))

@login_required()
def display(request, filename):
    print(filename)
    #class_id = get_object_or_404(Class, pk=pk)
    with open(media_root()+'file/'+filename, 'r') as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed
     