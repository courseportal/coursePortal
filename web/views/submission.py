from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse


from web.forms.submission import VideoForm, ExpositionForm, NoteForm, \
    ExampleForm
from web.models import Note, Video, Exposition, Example
from knoatom.view_functions import get_breadcrumbs
from web.views.view_functions import get_navbar_context, web_breadcrumb_dict

@login_required()
def video_submit(request, pk):
    """
    This is the view for video submission.
        
    """
    success_url = request.GET.get('next', None) # Redirection URL
    if 'add-another' in request.POST:
        success_url = reverse('video_submit')
    context = get_navbar_context()
    context.update(
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    form_kwargs = {'user': request.user}
    if pk:
        video =  get_object_or_404(Video, pk=pk)
        form_kwargs.update({'instance':video})
    else:
        video = None
    
    if request.method == 'POST':
        form = VideoForm(request.POST, **form_kwargs)
        
        if form.is_valid():
            obj = form.save()
            messages.success(
                request,
                _('The video has been submitted correctly.')
            )
            if success_url is not None:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(obj.get_absolute_url())
        else:
            messages.warning(request, _('Error submitting the video.'))
    else:
        form = VideoForm(**form_kwargs)
    
    context.update({
        'object':video,
        'form':form,
        'success_url':success_url
    })

    return render(request, 'web/home/video_submit.html', context)


@login_required()
def note_submit(request, pk):
    r"""
    This is the view for the lecture note submit feature.
    """
    success_url = request.GET.get('next', None)
    if 'add-another' in request.POST:
        success_url = reverse('note_submit')
    context = get_navbar_context()
    context.update(
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    form_kwargs = {'user':request.user}
    if pk:
        note = get_object_or_404(Note, pk=pk)
        form_kwargs.update({'instance':note})
    else:
        note = None

    if request.method == 'POST': # If the form has been submitted...
        form = NoteForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():    # All validation rules pass
            obj = form.save()
            messages.success(
                request,
                _('The note has been submitted correctly.')
            )
            if success_url is not None:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(obj.get_absolute_url())
            
        else:
            messages.warning(request, _('Error submitting the note.'))
    else:
        form = NoteForm(**form_kwargs)
        
    context.update({
        'object':note,
        'form':form,
        'success_url':success_url
    })

    return render(request, 'web/home/note_submit.html', context)
    
@login_required()
def example_submit(request, pk):
    r"""
    This is the view for the example submit feature.
    """
    success_url = request.GET.get('next', None)
    if 'add-another' in request.POST:
        success_url = reverse('example_submit')
    context = get_navbar_context()
    context.update(
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    form_kwargs = {'user':request.user}
    if pk:
        example = get_object_or_404(Example, pk=pk)
        form_kwargs.update({'instance':example})
    else:
        example = None
    
    if request.method == 'POST': # If the form has been submitted...
        form = ExampleForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():    # All validation rules pass
            obj = form.save()
            messages.success(
                request,
                _('The example has been submitted correctly.')
            )
            if success_url is not None:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(obj.get_absolute_url())
        else:
            messages.warning(request, _('Error submitting the example.'))
    else:
        form = ExampleForm(**form_kwargs)
        
    context.update({
        'object':example,
        'form':form,
        'success_url':success_url
    })

    return render(request, 'web/home/example_submit.html', context)


@login_required()
def exposition_submit(request, pk):
    r"""
    This is the view for the exposition submit feature.
    """
    success_url = request.GET.get('next', None)
    if 'add-another' in request.POST:
        success_url = reverse('expo_submit')
    context = get_navbar_context()
    context.update(
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )

    form_kwargs = {'user':request.user}
    if pk:
        exposition = get_object_or_404(Exposition, pk=pk)
        form_kwargs.update({'instance':exposition})
    else:
        exposition = None
    
    if request.method == 'POST': # If the form has been submitted...
        form = ExpositionForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():    # All validation rules pass
            obj = form.save()
            messages.success(
                request,
                _('The exposition has been submitted correctly.')
            )
            if success_url is not None:
                return HttpResponseRedirect(success_url)
            else:
                return HttpResponseRedirect(obj.get_absolute_url())
            
        else:
            messages.warning(request, _('Error submitting the exposition.'))
    else:
        form = ExpositionForm(**form_kwargs)
        
    context.update({
        'object':exposition,
        'form':form,
        'success_url':success_url
    })
    
    return render(request, 'web/home/expo_submit.html', context)