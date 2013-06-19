from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError, HttpResponseBadRequest
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404
import json
from web.models import *

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
		

@login_required()
def voteGeneral(request,item ,item_id, vote_type):
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	if request.user.is_authenticated():
		if item == '1':
			e = get_object_or_404(Exposition, id=item_id)
		elif item == '2':
			e = get_object_or_404(LectureNote, id=item_id)
		elif item == '3':
			e = get_object_or_404(Example, id=item_id)
		elif item == '4':
			e = get_object_or_404(Submission, id=item_id)
		else:
			HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad item type, must be one of {1,2,3,4}'}), mimetype="application/json")
		
		try:
			if item == '1':
				vote_example = VoteExposition.objects.filter(user=request.user).get(example=e)
			elif item == '2':
				vote_example = VoteLectureNote.objects.filter(user=request.user).get(example=e)
			elif item == '3':
				vote_example = VoteExample.objects.filter(user=request.user).get(example=e)
			else:
				vote_example = VoteVideo.objects.filter(user=request.user).get(example=e)

		# Check if the previous vote arees with the new vote
		# Update e.votes and vote_example accordingly
			if vote_type == '1':
				if vote_example.vote == 1:
					return HttpResponse(json.dumps({'result': False, 'votes': e.votes,'id':e.id}), mimetype="application/json")
				elif vote_example.vote == -1:
					vote_example.vote = 1
					vote_example.save()
					e.votes +=2
					e.save()
					# update user_rate as well
					user_rate = UserRating.objects.get(user=e.owner)
					user_rate.VoteUp += 1
					user_rate.VoteDown += 1
					user_rate.rating += 2
					user_rate.save()
					# update current user rating
					cur_user_rate = UserRating.objects.get(user=request.user)
					rating = cur_user_rate.rating
					return HttpResponse(json.dumps({'result': True,'requestUserRating': rating ,'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")

			elif vote_type == '0':
				if vote_example.vote == -1:
					return HttpResponse(json.dumps({'result': False, 'votes': e.votes,'id':e.id}), mimetype="application/json")
				elif vote_example.vote == 1:
					vote_example.vote = -1
					vote_example.save()
					e.votes -=2
					e.save()
					# update user_rate as well
					user_rate = UserRating.objects.get(user=e.owner)
					user_rate.VoteUp -= 1
					user_rate.VoteDown -= 1
					user_rate.rating -= 2
					user_rate.save()
					# update current user rating
					cur_user_rate = UserRating.objects.get(user=request.user)
					rating = cur_user_rate.rating
					return HttpResponse(json.dumps({'result': True,'requestUserRating': rating ,'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")
			else:
				print("something wrong with vote_type!!!")
		except (VoteExposition.DoesNotExist, VoteLectureNote.DoesNotExist, VoteExample.DoesNotExist, VoteVideo.DoesNotExist):
			if item == '1':
				vote_example = VoteExposition.objects.create(user=request.user,example=e, vote=1)
			elif item == '2':
				vote_example = VoteLectureNote.objects.create(user=request.user,example=e, vote=1)
			elif item == '3':
				vote_example = VoteExample.objects.create(user=request.user,example=e, vote=1)
			else:
				vote_example = VoteVideo.objects.create(user=request.user,example=e, vote=1)

			if vote_type == '1':
				vote_example.vote = 1
				vote_example.save()
				e.votes +=1
				e.save()
				# update user_rate as well
				user_rate = UserRating.objects.get(user=e.owner)
				user_rate.VoteUp += 1
				user_rate.rating += 1
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'requestUserRating': rating ,'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")
			elif vote_type == '0':
				vote_example.vote = -1
				vote_example.save()
				e.votes -=1
				e.save()
				# update user_rate as well
				user_rate = UserRating.objects.get(user=e.owner)
				user_rate.VoteDown -= 1
				user_rate.rating -= 1
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'requestUserRating': rating , 'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")

			else:
				print("something wrong with vote_type!!!")

	print("should not be GET")
	return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You must be authenticated'}), mimetype="application/json")
