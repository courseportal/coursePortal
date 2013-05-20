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
