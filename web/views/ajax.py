from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseServerError
from django.template import RequestContext, loader
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


def voteExample(request, example_id, vote_type):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    if request.user.is_authenticated():
        e = Example.objects.get(id=example_id)
        if vote_type == '1':
            if request.user.votes.example_vote_up:
                e.votes +=0
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': False, 'votes': e.votes}), mimetype="application/json")
            elif request.user.votes.example_vote_down:
                request.user.votes.example_vote_down = False
                request.user.votes.example_vote_up = True
                e.votes += 2
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': True,'votes': e.votes}), mimetype="application/json")
            elif request.user.votes.example_vote_up == False:
                request.user.votes.example_vote_up = True
                e.votes += 1
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': True, 'votes': e.votes}), mimetype="application/json")
            else:
                print("Error")
                return HttpResponseServerError(json.dumps({'result': False, 'error': 'error looking up your voting example information'}), mimetype="application/json")
        elif vote_type == '0':
            if request.user.votes.example_vote_down:
                e.votes -=0
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': False, 'votes': e.votes}), mimetype="application/json")
            elif request.user.votes.example_vote_up:
                request.user.votes.example_vote_up = False
                request.user.votes.example_vote_down = True
                e.votes -= 2
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': True, 'votes': e.votes}), mimetype="application/json")
            elif request.user.votes.example_vote_down == False:
                request.user.votes.example_vote_down = True
                e.votes -= 1
                e.save()
                request.user.votes.save()
                return HttpResponse(json.dumps({'result': True, 'votes': e.votes}), mimetype="application/json")
            else:
                print("Error")
                return HttpResponseServerError(json.dumps({'result': False, 'error': 'error looking up your voting example information'}), mimetype="application/json")
        else:
            print("something wrong with vote_type!!!")

    print("should not be GET")
    return HttpResponseForbidden(json.dumps({'result': False, 'error': 'You must be authenticated'}), mimetype="application/json")
