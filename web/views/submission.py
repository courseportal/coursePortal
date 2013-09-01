import json
import csv
import os
import hashlib
import re
import random
import string

from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseForbidden)
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

from web.forms.edit_class import DataImportForm
from knoatom.settings.development import MEDIA_ROOT
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError

from web.forms.submission import (ContentForm, YoutubeVideoForm, LinkForm,
                                  UploadedFileForm)
from knoatom.view_functions import get_breadcrumbs, render_to_json_response
from web.views.view_functions import get_navbar_context, web_breadcrumb_dict
from web.models import Content, YoutubeVideo, Link, UploadedFile, Class, Atom
from django.contrib.auth.models import User

def validate_umich_email(value):
    is_valid_email = True
    regex_umich_email = re.compile('\w*@umich.edu')
    if not regex_umich_email.match(value):
        is_valid_email = False
    return is_valid_email

def validate_username(username, email):
    is_valid_username = True
    if (cmp(username, email.split('@')[0]) !=0):
        is_valid_username = False
    return is_valid_username

def validate_full_name(first_name, last_name):
    is_valid_full_name = True
    if ((first_name.find('@') != -1) or (last_name.find('@') != -1)):
        is_valid_full_name = False
    return is_valid_full_name

def validate_handle_uploaded_file(f, request, classId):
    with open(f,'Ub') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        rownum = 0
        
        for row in datareader:
            if rownum == 0:
                
                rownum +=1
            else:
                if( validate_umich_email(row[3]) == False):
                    print("not valid email")
                    return -1
                else:
                    print("valid email")
                
                if( validate_username(row[2], row[3]) == False):
                    print("not valid username")
                    return -1
                else:
                    print("valid username")
                
                if ( validate_full_name(row[0], row[1])== False):
                    print("not valid name")
                    return -1
                else:
                    print("valid name")
            rownum += 1

    csvfile.close()
    return 1
  
def handle_uploaded_file(f, request, classId):
    with open(f,'Ub') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        rownum = 0
                
        for row in datareader:
            if rownum == 0:

                rownum +=1
            else:
                try:
                    exist_user = User.objects.get(email__exact=row[3])
                except User.DoesNotExist:
                    exist_user = None
                if not exist_user:
                    password = User.objects.make_random_password()

                    created_user = User.objects.create_user(
                                                           row[2] , row[3],
                                                            password,
                                                            )
                    
                    User.objects.filter(email=row[3]).update(first_name = row[0],last_name = row[1], username = row[2], is_active = False, date_joined=datetime.now())
                    
                    ClassIn = Class.objects.get(id=classId)
                    created_user.enrolled_classes.add(ClassIn)
                    
                    m = hashlib.md5()
                    m.update(created_user.email + str(created_user.date_joined).split('.')[0])
                    send_mail(
                              subject=_('KnoAtom Registration and Class Enrollment for[' + ClassIn.title + ']'),
                              message=(_('You have successfully registered at '
                                         'knoatom.eecs.umich.edu with the username: ') +
                                       created_user.username + ' and default password: ' + password +
                                       _('. Please validate your account by going to http://')+
                                       request.META['HTTP_HOST']+'/validate?email='+
                                       created_user.email + '&validation=' + m.hexdigest() +
                                       _(' . If you did not process this registration, '
                                         'please contact us as soon as possible.\n\n-- The '
                                         'Management')
                                       ),
                              from_email='knoatom-noreply@gmail.com',
                              recipient_list=[created_user.email, settings.EMAIL_HOST_USER],     # 
                              fail_silently=False
                              )
                else:
                    ClassIn = Class.objects.get(pk=classId)
                    try:
                        exist_ClassIn = exist_user.enrolled_classes.get(pk=classId)
                    except Class.DoesNotExist:
                        exist_ClassIn = None
                    if not exist_ClassIn:
                        exist_user.enrolled_classes.add(ClassIn)
                        send_mail(
                                  subject=_('Class Enrolled'),
                                  message=(_('You have successfully enrolled ' + ClassIn.title +
                                             'at knoatom.eecs.umich.edu with the username: ') +
                                           exist_user.username +
                                           _(' . If you have not enrolled in the class, '
                                             'please contact us as soon as possible.\n\n-- The '
                                             'Management')
                                           ),
                                  from_email='knoatom-noreply@gmail.com',
                                  recipient_list=[exist_user.email, settings.EMAIL_HOST_USER],     #
                                  fail_silently=False
                                  )
                rownum += 1




@login_required()
def upload_file(request, classId):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            data = request.FILES['file']
            path = default_storage.save('tmp/data.csv', ContentFile(data.read()))
            tmp_file = os.path.join(MEDIA_ROOT, path)
            classId = request.POST['classId']
            is_valid_form = validate_handle_uploaded_file(tmp_file, request, classId)
            if (is_valid_form == 1):
                handle_uploaded_file(tmp_file, request, classId)
            os.remove(tmp_file)
            default_storage.delete(path)
            return is_valid_form
        else:
            return -1
    else:
        return 0


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
def submit_content(request, pk=None):       # class_pk=None
    r"""This is the main view for submitting content."""
    if pk is None:
        obj = None
    else:
        obj = get_object_or_404(Content, pk=pk)
        if not (request.user.is_superuser or request.user == obj.owner):
            return HttpResponseForbidden()
    pk = request.GET.get('pk', None) # Resetting pk
    class_pk = request.GET.get('class_pk', None)
    atom_id = request.GET.get('atom_id', None)
    form_kwargs_atom_id = { 'atom_id':atom_id }
    if class_pk is None:
        class_obj = None
    else:
        class_obj = get_object_or_404(Class, id=class_pk)

    content_type = request.GET.get('type', None)

    if request.is_ajax():
        if content_type is None:
            return process_content(request, obj, atom_id)
        elif content_type == 'video':
            return process_subcontent(request, obj, YoutubeVideo,
                                      YoutubeVideoForm, pk)
        elif content_type == 'link':
            return process_subcontent(request, obj, Link, LinkForm, pk)
        elif content_type == 'file':
            return process_subcontent(request, obj, UploadedFile,
                                      UploadedFileForm, pk)
        elif content_type == 'class_atom':
            if class_obj is not None:
                class_category_list = class_obj.category_set.all()
                class_atom_list = []
                for i in class_category_list:
                    class_atom_list.extend(list(i.child_atoms.all()))
                class_atom_list_set = list(set(tuple(class_atom_list)))
                
                data = serializers.serialize('json', class_atom_list_set)
                return HttpResponse(data, 'application/json')
            else:
                atom_list = Atom.objects.all()
                print("!!!!!!!!!!!")
                data = serializers.serialize('json', atom_list)
                return HttpResponse(data, 'application/json')
            #return HttpResponseBadRequest()
        return HttpResponseBadRequest()
    else: # Not AJAX Request
        context = {};
        if content_type == 'file':
            context = process_file(request, obj, pk)
        elif content_type is not None or pk is not None:
            return HttpResponseBadRequest()

        form = ContentForm(instance=obj, user=request.user, atom_id=atom_id)
        atom_list = Atom.objects.all();
        is_class_owner_or_instructor = False;
        if (request.user.classes_authored.exists() or request.user.allowed_classes.exists() or request.user.is_superuser):
            is_class_owner_or_instructor = True;

        context.update(
                       get_navbar_context()
                       )
        context.update(
                       get_breadcrumbs(request.path, web_breadcrumb_dict)
                       )
        context.update({
                       'is_class_owner_or_instructor': is_class_owner_or_instructor,
                       'atom_list': atom_list,
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

def process_content(request, obj, atom_id):
    form_kwargs = { 'user':request.user, 'instance':obj, 'atom_id':atom_id }
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