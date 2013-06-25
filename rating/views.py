from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from web.models import *
from rating.ratings import *
from rating.models import *

import json


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
				if vote_example.vote == vote_up_delta_rating():
					return HttpResponse(json.dumps({'result': False, 'votes': e.votes,'id':e.id}), mimetype="application/json")
				elif vote_example.vote == vote_down_delta_rating():
					vote_example.vote = vote_up_delta_rating()
					vote_example.save()
					e.votes -= vote_down_delta_rating()
					e.votes += vote_up_delta_rating()
					e.save()
					# update user_rate as well
					user_rate = UserRating.objects.get(user=e.owner)
					user_rate.VoteUp += vote_up_delta_rating()
					user_rate.VoteDown -= vote_down_delta_rating()
					user_rate.rating -= vote_down_delta_rating()
					user_rate.rating += vote_up_delta_rating()
					user_rate.save()
					# update current user rating
					cur_user_rate = UserRating.objects.get(user=request.user)
					rating = cur_user_rate.rating
					return HttpResponse(json.dumps({'result': True,'requestUserRating': rating ,'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")

			elif vote_type == '0':
				if vote_example.vote == vote_down_delta_rating():
					return HttpResponse(json.dumps({'result': False, 'votes': e.votes,'id':e.id}), mimetype="application/json")
				elif vote_example.vote == vote_up_delta_rating():
					vote_example.vote = vote_down_delta_rating()
					vote_example.save()
					e.votes -= vote_up_delta_rating()
					e.votes += vote_down_delta_rating()
					e.save()
					# update user_rate as well
					user_rate = UserRating.objects.get(user=e.owner)
					user_rate.VoteUp -= vote_up_delta_rating()
					user_rate.VoteDown += vote_down_delta_rating()
					user_rate.rating -= vote_up_delta_rating()
					user_rate.rating += vote_down_delta_rating()
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
				vote_example.vote = vote_up_delta_rating()
				vote_example.save()
				e.votes += vote_up_delta_rating()
				e.save()
				# update user_rate as well
				user_rate = UserRating.objects.get(user=e.owner)
				user_rate.VoteUp += vote_up_delta_rating()
				user_rate.rating += vote_up_delta_rating()
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'requestUserRating': rating ,'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")
			elif vote_type == '0':
				vote_example.vote = vote_down_delta_rating()
				vote_example.save()
				e.votes += vote_down_delta_rating()
				e.save()
				# update user_rate as well
				user_rate = UserRating.objects.get(user=e.owner)
				user_rate.VoteDown += vote_down_delta_rating()
				user_rate.rating += vote_down_delta_rating()
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'requestUserRating': rating , 'votes': e.votes,'id':e.id, 'itemType':item,}), mimetype="application/json")

			else:
				print("something wrong with vote_type!!!")

	print("should not be GET")
	return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You must be authenticated'}), mimetype="application/json")
