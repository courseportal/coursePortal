from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.core.mail import send_mail, BadHeaderError
import json
from web.forms.submission import testModalForm
from web.models import *
from rating.models import UserRating

@login_required()
def vote(request, submission_id, vote_category, vote_value):
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	if request.user.is_authenticated():
		s = Submission.objects.get(id=submission_id)
		curr_v = Vote.objects.filter(submission=s).filter(user=request.user).filter(v_category=vote_category)
		print("Vote() function has been called!")
		if len(curr_v) == 1:
			curr_v = curr_v[0]
			curr_v.rating = vote_value
			curr_v.save()
		elif len(curr_v) == 0:
			curr_v = Vote()
			curr_v.submission = s
			curr_v.user = request.user
			curr_v.rating = vote_value
			curr_v.v_category = VoteCategory.objects.get(id=vote_category)
			curr_v.save()
		else:
			return HttpResponseServerError(json.dumps({'result': False, 'error': 'error looking up your voting information'}), mimetype="application/json")
		return HttpResponse(json.dumps({'result': True}), mimetype="application/json")
	return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You must be authenticated'}), mimetype="application/json")
	
@login_required()
def delete_content(request, item, item_id):
	r"""
	This view handles the deletion of content from the content list with AJAX
	
	The first argument is the item type ``item``:
		*	1 = Exposition
		*	2 = LectureNote
		*	3 = Example
		*	4 = Submission
		
	The next argument is the item_id for whatever type of content we are going to delete
	
	"""
	
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	# Get the correct object
	if item == '1':
		obj = get_object_or_404(Exposition, id=item_id)
	elif item == '2':
		obj = get_object_or_404(LectureNote, id=item_id)
	elif item == '3':
		obj = get_object_or_404(Example, id=item_id)
	elif item == '4':
		obj = get_object_or_404(Submission, id=item_id)
	else:
		return HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad item type, must be one of {1,2,3,4}'}), mimetype="application/json")
	
	# Check that the user has permission to delete the object
	if not (request.user.is_superuser or request.user == obj.owner):
		return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You are not authorized to perform this action'}), mimetype="application/json")
		
	# We are authorized to perform this action
	obj_id = obj.id
	obj.delete()
	cur_user_rate = UserRating.objects.get(user=request.user).rating
	# Return and report a success with the correct response variables
	return HttpResponse(json.dumps({'result': True, 'itemType': item, 'id':obj_id, 'requestUserRating':cur_user_rate}), mimetype="application/json")

@login_required()
def sticky_content(request, class_id, item, item_id):
	r"""
	This view handles the sticking/unsticking of content from the content list with AJAX.
	
	The first agrument is the id of the current class.
	
	This view also takes in the item type ``item``:
		*	1 = Exposition
		*	2 = LectureNote
		*	3 = Example
		*	4 = Submission
		
	It takes in the item_id for whatever type of content we are going to sticky.
	
	It takes in the boolean stickied.  If stickied then we will unsticky the object, otherwise we will sticky the object.
	"""
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	selected_class = get_object_or_404(Class, id=class_id)
	if not (request.user.is_superuser or request.user == selected_class.author or selected_class.allowed_users.filter(id=request.user.id).exists()):
		return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You are not authorized to perform this action'}), mimetype="application/json")

	# At this point we know they are authorized to stick/unstick topics
	if item == '1':
		obj = get_object_or_404(Exposition, id=item_id)
	elif item == '2':
		obj = get_object_or_404(LectureNote, id=item_id)
	elif item == '3':
		obj = get_object_or_404(Example, id=item_id)
	elif item == '4':
		obj = get_object_or_404(Submission, id=item_id)
	else:
		return HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad item type, must be one of {1,2,3,4}'}), mimetype="application/json")
		
	if obj.classes_stickied_in.filter(id=selected_class.id).exists():
		obj.classes_stickied_in.remove(selected_class)
		return HttpResponse(json.dumps({'result': True, 'itemType': item, 'id':obj.id, 'name':obj.__unicode__(), 'stickied':False}), mimetype="application/json")
	else:
		obj.classes_stickied_in.add(selected_class)
		return HttpResponse(json.dumps({'result': True, 'itemType': item, 'id':obj.id, 'name':obj.__unicode__(), 'stickied':True}), mimetype="application/json")