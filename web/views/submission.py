from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
import json
from web.forms.submission import SubmissionForm, ExpoForm, LectureNoteForm, ExampleForm
from web.models import AtomCategory, LectureNote, Submission, Class, BaseCategory, Exposition, Example

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

@login_required()
def index(request, sid):
    """
    This function does a lot of really cool things
    
    """
    #Get the "top level" categories
    top_level_categories = BaseCategory.objects.filter(parent_categories=None)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, error_class=PlainErrorList)
        if sid:
            if form.is_valid():
                sub = Submission.objects.get(pk=sid)
                sub.title = form.cleaned_data['title']
                sub.content = form.cleaned_data['content']
                sub.video = json.dumps(form.cleaned_data['video'].split(' '))
                sub.tags = form.cleaned_data['tags']
                sub.save()
                messages.success(request, 'Successfully saved.')
                return HttpResponseRedirect(reverse('post', args=[s.id])) 
            messages.warning(request, 'Error saving. Fields might be invalid.')
        else:
            if form.is_valid():
                s = Submission(owner=request.user)
                s.title = form.cleaned_data['title']
                s.content = form.cleaned_data['content']
                s.video = json.dumps(form.cleaned_data['video'].split(' '))
                s.save()
                s.tags = form.cleaned_data['tags']
                s.save()
                return HttpResponseRedirect(reverse('post', args=[s.id]))
            messages.warning(request, 'Error submitting.')
    else:
        if sid:
            sub = Submission.objects.get(pk=sid)
            if sub.video: video = ' '.join(json.loads(sub.video))
            else: video = ''
            i_data = {
                'title': sub.title,
                'content': sub.content,
                'video': video,
                'tags': sub.tags.all(),
            }
            form = SubmissionForm(initial=i_data, error_class=PlainErrorList)
        else:
            form = SubmissionForm(error_class=PlainErrorList)

    if sid: form_action = reverse('submit', args=[sid])
    else: form_action = reverse('submit')
    

    t = loader.get_template('web/home/submit.html')
    c = RequestContext(request, {
		'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'top_level_categories': top_level_categories,
        'form': form,
        #'child_categories': child_categories,
        #'parent_categories': L,
    })
    return HttpResponse(t.render(c))
	
@login_required()
def note_submit(request):
	r"""
	This is the view for the lecture note submit feature.
	"""
	
	# Get "top level" categories
	top_level_categories = BaseCategory.objects.filter(parent_categories=None)

	if request.method == 'POST': # If the form has been submitted...
		form = LectureNoteForm(request.POST, request.FILES)
		if form.is_valid():	# All validation rules pass
			note = LectureNote(owner=request.user)
			note.file = request.FILES['file']
			note.atom = form.cleaned_data['atom']
			note.filename = form.cleaned_data['filename']
			note.save()
			
			return HttpResponseRedirect(reverse('home')) #should change this
		messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = LectureNoteForm() # Create an unbound form

	return render(request, 'web/home/note_submit.html', {
		'form': form,
		'top_level_categories': top_level_categories,
		'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
	})
	
@login_required()
def example_submit(request):
	r"""
	This is the view for the example submit feature.
	"""
	
	# Get "top level" categories
	top_level_categories = BaseCategory.objects.filter(parent_categories=None)

	if request.method == 'POST': # If the form has been submitted...
		form = ExampleForm(request.POST, request.FILES)
		if form.is_valid():	# All validation rules pass
			example = Example(owner=request.user)
			example.file = request.FILES['file']
			example.atom = form.cleaned_data['atom']
			example.filename = form.cleaned_data['filename']
			example.save()
			
			return HttpResponseRedirect(reverse('home')) #should change this
		messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = ExampleForm() # Create an unbound form

	return render(request, 'web/home/example_submit.html', {
		'form': form,
		'top_level_categories': top_level_categories,
		'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
	})
    
@login_required()
def exposition(request):
	
	# Get "top level" categories
	top_level_categories = BaseCategory.objects.filter(parent_categories=None)

	if request.method == 'POST': # If the form has been submitted...
		form = ExpoForm(request.POST) # A form bound to the POST data
		if form.is_valid():	# All validation rules pass
		
			# Creating the exposition from the data
			expo = Exposition(owner=request.user)
			expo.title = form.cleaned_data['title']
			expo.link = form.cleaned_data['link']
			expo.atom = form.cleaned_data['atom']
			expo.save()
			
			return HttpResponseRedirect(reverse('home')) #should change this
		messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = ExpoForm() # Create an unbound form
	
	return render(request, 'web/home/expo_submit.html', {
		'form': form,
		'top_level_categories': top_level_categories,
		'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
	})