import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponse, HttpResponseRedirect,   
    HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden)
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from web.forms.submission import (ContentForm, YoutubeVideoForm, LinkForm, 
    UploadedFileForm)
from knoatom.view_functions import get_breadcrumbs, render_to_json_response
from web.views.view_functions import get_navbar_context, web_breadcrumb_dict
from web.models import Content, YoutubeVideo, Link, UploadedFile

@login_required()
def delete_content(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    content_type = request.GET.get('type', None)
    pk = request.GET.get('pk', None)
    type_dict = {'content':Content, 'video':YoutubeVideo, 'link':Link, 
        'file':UploadedFile}
    Model = type_dict.get(content_type, None)
    if Model is None or pk is None:
        return HttpResponseBadRequest()
    obj = get_object_or_404(Model, pk=pk)
    deleted = False
    title = obj.title
    if request.user.is_superuser:
        obj.delete()
        deleted = True
    elif content_type == 'content':
        if request.user == obj.owner:
            obj.delete()
            deleted = True
    else:
        if request.user == obj.content.owner:
            obj.delete()
            deleted = True
    if deleted:
        context = {
            'message':('<div class="alert alert-success">' + 
                _('Successfully deleted {}.'.format(title)) +'</div>')
        }
        return render_to_json_response(context)
    else:
        context = {
            'message':('<div class="alert alert-error">' + 
                _('Failed to delete {}.'.format(title)) +'</div>')
        }
        return render_to_json_response(context, status=400)
        
@login_required()
def submit_content(request, pk=None):
    r"""This is the main view for submitting content."""
    if pk is None:
        obj = None
    else:
        obj = get_object_or_404(Content, pk=pk)
        if not (request.user.is_superuser or request.user == obj.owner):
            return HttpResponseForbidden()
    pk = request.GET.get('pk', None) # Resetting pk
    content_type = request.GET.get('type', None)
    if request.is_ajax():
        if content_type is None:
            return process_content(request, obj)
        elif content_type == 'video':
            return process_subcontent(request, obj, YoutubeVideo, 
                YoutubeVideoForm, pk)
        elif content_type == 'link':
            return process_subcontent(request, obj, Link, LinkForm, pk)
        elif content_type == 'file':
            return process_subcontent(request, obj, UploadedFile, 
                UploadedFileForm, pk)
            return HttpResponseBadRequest()
        return HttpResponseBadRequest()
    else: # Not AJAX Request
        context = {};
        if content_type == 'file':
            context = process_file(request, obj, pk)
        elif content_type is not None or pk is not None:
            return HttpResponseBadRequest()

        form = ContentForm(instance=obj, user=request.user)
        context.update(
            get_navbar_context()
        )
        context.update(
            get_breadcrumbs(request.path, web_breadcrumb_dict)
        )
        context.update({
            'content_object':obj,
            'form':form,
            'empty_video_form':YoutubeVideoForm(content=obj),
            'empty_link_form':LinkForm(content=obj),
            'empty_file_form':UploadedFileForm(content=obj),
        })
        if obj is not None:
            context.update({'pk':obj.pk})
        return render(request, 'web/content_form.html', context)
            
def process_file(request, content, pk):
    context = {}
    if pk is not None:
        obj = get_object_or_404(UploadedFile, pk=pk)
    else:
        obj = None
    form_kwargs = {'instance':obj, 'content':content}
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES, **form_kwargs)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 
                "Successfully saved {}".format(obj.title)
            )
        else: #Not valid
            context['file_form'] = form
            if pk is not None:
                context['file_pk'] = pk
            messages.error(request, "Error saving file.")
    return context
    
     
def process_subcontent(request, content, Model, Form, pk):
    if pk is not None:
        obj = get_object_or_404(Model, pk=pk)
    else:
        obj = None
    form_kwargs = {'instance':obj, 'content':content}
    if request.method == 'POST': # Files should not be POST'ed to here.
        form = Form(request.POST, **form_kwargs)
        if form.is_valid():
            obj = form.save()
            del form_kwargs['instance']
            form = Form(**form_kwargs)
            template = loader.get_template('web/form_template.html')
            c = RequestContext(request, {'form':Form(**form_kwargs)})
            context = {
                'title':obj.title,
                'pk':obj.pk,
                'message':('<div class="alert alert-success">' + 
                    _('Successfully saved {}.'.format(str(obj))) +'</div>'),
                'form_html':template.render(c),
            }
            return render_to_json_response(context, status=201)
        else: #Not valid
            template = loader.get_template('web/form_template.html')
            c = RequestContext(request, {'form':form})
            context = {
                'message':('<div class="alert alert-error">' +
                           _('Error saving object.') + '</div>'),
                'form_html':template.render(c),
            }
            return render_to_json_response(context, status=400)
    elif request.method == 'GET': # GET is valid for files however.
        template = loader.get_template('web/form_template.html')
        c = RequestContext(request, {'form':Form(**form_kwargs)})
        return render_to_json_response({'form':template.render(c)})
    else:
        data = json.dumps(_('Request type must be POST or GET'))
        response_kwargs = {'content_type':'application/json'}
        return HttpResponseNotAllowed(['POST', 'GET'], data, **response_kwargs)
        
def process_content(request, obj):
    form_kwargs = {'instance':obj, 'user':request.user}
    if request.method == 'POST':
        form = ContentForm(request.POST, **form_kwargs)
        if form.is_valid():
            obj = form.save()
            form_kwargs['instance'] = obj
            template = loader.get_template('web/form_template.html')
            c = RequestContext(request, {'form':ContentForm(**form_kwargs)})
            context = {
                'title':obj.title,
                'pk':obj.pk,
                'message':('<div class="alert alert-success">' + 
                    _('Successfully saved content') +'</div>'),
                'form_html':template.render(c),
            }
            return render_to_json_response(context, status=201) 
        else:
            template = loader.get_template('web/form_template.html')
            c = RequestContext(request, {'form':form})
            context = {
                'message':('<div class="alert alert-error">' + 
                    _('Error saving content.') + '</div>'),
                'form_html':template.render(c),
            }
            return render_to_json_response(context, status=400)  
    else: # Return a not allowed response.
        data = json.dumps(_('The request type must be "POST"'))
        response_kwargs = {'content_type':'application/json'}
        return HttpResponseNotAllowed(['POST'], data, **response_kwargs)