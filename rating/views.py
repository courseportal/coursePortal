from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from knoatom.view_functions import render_to_json_response
from web.models import *
from pybb.models import Topic
from rating.ratings import *
from rating.models import *

import json

@login_required()
def vote(request, atom_id, item, item_id, vote_type):
    r"""This voting system is a refactored version of the original voting system written by Taoran."""
    atom_object = get_object_or_404(Atom, id=atom_id)
    if item == 'exposition':
        content_object = get_object_or_404(Exposition, id=item_id)
    elif item == 'note':
        content_object = get_object_or_404(Note, id=item_id)
    elif item == 'example':
        content_object = get_object_or_404(Example, id=item_id)
    elif item == 'video':
        content_object = get_object_or_404(Video, id=item_id)
    elif item == 'topic':
        content_object = get_object_or_404(Topic, id=item_id)
    else:
        raise Http404
        
    vote = content_object.vote_set.get_or_create(atom=atom_object, user=request.user)[0]
    if (vote.vote > 0 and vote_type == 'up') or (vote.vote < 0 
            and vote_type == 'down'):
        context = {'result': False, 'alert':'You have already voted {}.'.format(vote_type)}
        return render_to_json_response(context)
    else:
        delta = 0
        if vote_type == 'up':
            if vote.vote != 0:
                delta = -1*vote_down_delta_rating()
            delta += vote_up_delta_rating()
        elif vote_type == 'down':
            if vote.vote != 0:
                delta = -1*vote_up_delta_rating()
            delta += vote_down_delta_rating()
        else:
            raise Http404
        vote.vote += delta
        vote.save()
        if item != 'topic':
            user_rating = UserRating.objects.get(user=content_object.owner)
        else:
            user_rating = UserRating.objects.get(user=content_object.user)
        
    
        user_rating.VoteUp += vote_up_delta_rating()
        user_rating.VoteDown -= vote_down_delta_rating()
        user_rating.rating += delta
        user_rating.save()
        votes = [v.vote for v in content_object.vote_set.filter(atom=atom_object)]
        context = {
            'result':True, 
            'votes':sum(votes),
            'id':content_object.id,
            'item':item
        }
        # update current user rating
        if user_rating.user == request.user:
            context.update({'user_rating': user_rating.rating})    
        return render_to_json_response(context)


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
