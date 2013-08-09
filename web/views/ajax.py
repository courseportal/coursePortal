from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import ugettext_lazy as _
import json
from web.models import Example, Exposition, Note, Video, Class
from knoatom.view_functions import render_to_json_response
from rating.models import UserRating
	
@login_required()
def delete_content(request, item, pk):
	r"""
	This view handles the deletion of content from the content list with AJAX
	
	The first argument is the item type ``item``.
		
	The next argument is the pk for whatever type of content we are going to delete
	
	"""
	
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	# Get the correct object
	if item == 'exposition':
		obj = get_object_or_404(Exposition, pk=pk)
	elif item == 'note':
		obj = get_object_or_404(Note, pk=pk)
	elif item == 'example':
		obj = get_object_or_404(Example, pk=pk)
	elif item == 'video':
		obj = get_object_or_404(Video, pk=pk)
	else:
		return HttpResponseBadRequest(json.dumps({
				'result': False,
				'error':_('Bad item type')
			}), 
			mimetype="application/json"
		)
	
	# Check that the user has permission to delete the object
	if not (request.user.is_superuser or request.user == obj.owner):
		return HttpResponseForbidden(json.dumps({
				'result': False,
				'error': _('You are not authorized to perform this action')
			}),
			mimetype="application/json"
		)
		
	# We are authorized to perform this action
	obj.delete()
	cur_user_rate = UserRating.objects.get(user=request.user).rating
	# Return and report a success with the correct response variables
	context = {
		'result': True,
		'item': item,
		'id':pk,
		'user_rating':cur_user_rate
	}
	return render_to_json_response(context)

@login_required()
def sticky_content(request, class_id, item, item_id):
	r"""
	This view handles the sticking/unsticking of content from the content list with AJAX.
	
	The first agrument is the id of the current class.
	
	This view also takes in the item type ``item``.
	
	It takes in the item_id for whatever type of content we are going to sticky.
	
	It takes in the boolean stickied.  If stickied then we will unsticky the object, otherwise we will sticky the object.
	"""
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
		
	class_object = get_object_or_404(Class, id=class_id)
	if not (request.user.is_superuser or 
			request.user == class_object.author or
			class_object.allowed_users.filter(id=request.user.id).exists()):
		return HttpResponseForbidden(json.dumps({
				'result': False,
				'error': _('You are not authorized to perform this action')
			}),
			mimetype="application/json"
		)
	# At this point we know they are authorized to stick/unstick topics
	if item == 'exposition':
		obj = get_object_or_404(Exposition, id=item_id)
	elif item == 'note':
		obj = get_object_or_404(Note, id=item_id)
	elif item == 'example':
		obj = get_object_or_404(Example, id=item_id)
	elif item == 'video':
		obj = get_object_or_404(Video, id=item_id)
	else:
		return HttpResponseBadRequest(json.dumps({
				'result': False,
				'error': _('Bad item type.')
			}),
			mimetype="application/json"
		)
	
	context = {
		'result': True,
		'item': item,
		'id':obj.id,
		'name':obj.__unicode__()
	}
	if obj.classes_stickied_in.filter(id=class_object.id).exists():
		obj.classes_stickied_in.remove(class_object)
		context.update({'stickied':False})
	else:
		obj.classes_stickied_in.add(class_object)
		context.update({'stickied':True})
	return render_to_json_response(context)