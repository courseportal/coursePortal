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
                vote.voteUp += vote_up_delta_rating()
                vote.voteDown += vote_down_delta_rating()
            else:
                vote.voteUp += vote_up_delta_rating()
            delta += vote_up_delta_rating()
            
        elif vote_type == 'down':
            if vote.vote != 0:
                delta = -1*vote_up_delta_rating()
                vote.voteDown -= vote_down_delta_rating()
                vote.voteUp -= vote_up_delta_rating()
            else:
                vote.voteDown -= vote_down_delta_rating()
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
        votesUp = [v.voteUp for v in content_object.vote_set.filter(atom=atom_object)]
        votesDown = [v.voteDown for v in content_object.vote_set.filter(atom=atom_object)]
        context = {
            'result':True, 
            'votes':sum(votes),
            'votesUp': sum(votesUp),
            'votesDown': sum(votesDown),
            'id':content_object.id,
            'item':item
        }
        # update current user rating
        if user_rating.user == request.user:
            context.update({'user_rating': user_rating.rating})    
        return render_to_json_response(context)