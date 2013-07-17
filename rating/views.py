from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from web.models import *
from pybb.models import Topic
from rating.ratings import *
from rating.models import *

import json


@login_required()
def voteGeneral(request, item ,item_id, vote_type):
	if request.method != 'GET':
		return HttpResponseNotAllowed(['GET'])
	if request.user.is_authenticated():
		if item == 'exposition':
			e = get_object_or_404(Exposition, id=item_id)
		elif item == 'note':
			e = get_object_or_404(Note, id=item_id)
		elif item == 'example':
			e = get_object_or_404(Example, id=item_id)
		elif item == 'video':
			e = get_object_or_404(Video, id=item_id)
		elif item == 'topic':
			e = get_object_or_404(Topic, id=item_id)
		else:
			HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad item type'}), mimetype="application/json")
		
		try:
			if item == 'expositoin':
				vote_example = VoteExposition.objects.filter(user=request.user).get(example=e)
			elif item == 'note':
				vote_example = VoteNote.objects.filter(user=request.user).get(example=e)
			elif item == 'example':
				vote_example = VoteExample.objects.filter(user=request.user).get(example=e)
			elif item == 'video':
				vote_example = VoteVideo.objects.filter(user=request.user).get(example=e)
			else:
				vote_example = VoteTopic.objects.filter(user=request.user).get(example=e)

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
					if not item == 'topic':
						user_rate = UserRating.objects.get(user=e.owner)
					else:
						user_rate = UserRating.objects.get(user=e.user)
					user_rate.VoteUp += vote_up_delta_rating()
					user_rate.VoteDown -= vote_down_delta_rating()
					user_rate.rating -= vote_down_delta_rating()
					user_rate.rating += vote_up_delta_rating()
					user_rate.save()
					# update current user rating
					cur_user_rate = UserRating.objects.get(user=request.user)
					rating = cur_user_rate.rating
					return HttpResponse(json.dumps({'result': True,'user_rating': rating ,'votes': e.votes,'id':e.id, 'item':item,}), mimetype="application/json")

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
					if not item == 'topic':
						user_rate = UserRating.objects.get(user=e.owner)
					else:
						user_rate = UserRating.objects.get(user=e.user)
					user_rate.VoteUp -= vote_up_delta_rating()
					user_rate.VoteDown += vote_down_delta_rating()
					user_rate.rating -= vote_up_delta_rating()
					user_rate.rating += vote_down_delta_rating()
					user_rate.save()
					# update current user rating
					cur_user_rate = UserRating.objects.get(user=request.user)
					rating = cur_user_rate.rating
					return HttpResponse(json.dumps({'result': True,'user_rating': rating ,'votes': e.votes,'id':e.id, 'item':item,}), mimetype="application/json")
			else:
				HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad vote_type, must be one of {0, 1}'}), mimetype="application/json")
				
		except (VoteExposition.DoesNotExist, VoteNote.DoesNotExist, VoteExample.DoesNotExist, VoteVideo.DoesNotExist, VoteTopic.DoesNotExist):
			if item == 'exposition':
				vote_example = VoteExposition.objects.create(user=request.user,example=e, vote=1)
			elif item == 'note':
				vote_example = VoteNote.objects.create(user=request.user,example=e, vote=1)
			elif item == 'example':
				vote_example = VoteExample.objects.create(user=request.user,example=e, vote=1)
			elif item == 'video':
				vote_example = VoteVideo.objects.create(user=request.user,example=e, vote=1)
			else:
				vote_example = VoteTopic.objects.create(user=request.user, example=e, vote=1)

			if vote_type == '1':
				vote_example.vote = vote_up_delta_rating()
				vote_example.save()
				e.votes += vote_up_delta_rating()
				e.save()
				# update user_rate as well
				if not item == 'topic':
					user_rate = UserRating.objects.get(user=e.owner)
				else:
					user_rate = UserRating.objects.get(user=e.user)
				user_rate.VoteUp += vote_up_delta_rating()
				user_rate.rating += vote_up_delta_rating()
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'user_rating': rating ,'votes': e.votes,'id':e.id, 'item':item,}), mimetype="application/json")
			elif vote_type == '0':
				vote_example.vote = vote_down_delta_rating()
				vote_example.save()
				e.votes += vote_down_delta_rating()
				e.save()
				# update user_rate as well
				if not item == 'topic':
					user_rate = UserRating.objects.get(user=e.owner)
				else:
					user_rate = UserRating.objects.get(user=e.user)
				user_rate.VoteDown += vote_down_delta_rating()
				user_rate.rating += vote_down_delta_rating()
				user_rate.save()
				# update current user rating
				cur_user_rate = UserRating.objects.get(user=request.user)
				rating = cur_user_rate.rating
				return HttpResponse(json.dumps({'result': True,'user_rating': rating , 'votes': e.votes,'id':e.id, 'item':item,}), mimetype="application/json")

			else:
				HttpResponseBadRequest(json.dumps({'result': False, 'error': 'Bad vote_type, must be one of {0, 1}'}), mimetype="application/json")

	return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You must be authenticated'}), mimetype="application/json")
