from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader
import json
from web.models import Category, Submission, VoteCategory

def category(request, cat):
    """
    - Generates the view for a specific category
    - Creates the breadcrumbs for the page
    """
    try:
        category = Category.objects.get(id=cat)
    except Category.DoesNotExist:
        raise Http404
    parents = category.parent.all()
    breadcrumbs = [{'url': reverse('home'), 'title': 'Home'}]

    if len(parents) == 0:
        parent = category
        content = Submission.objects.filter( Q(tags=category) | Q(tags__in=category.child.distinct()) ).distinct()
    else:
        parent = parents[0]
        content = Submission.objects.filter( Q(tags=category) ).distinct()
        breadcrumbs.append({'url': reverse('category', args=[parent.id]), 'title': parent})

    breadcrumbs.append({'url': reverse('category', args=[category.id]), 'title': category})

    # un-json-fy the videos
    for c in content:
        if c.video: c.video = [v for v in json.loads(c.video)]

    if request.user.is_authenticated():
        for c in content:
            ratings = c.votes.filter(user=request.user)
            c.user_rating = {}
            if ratings.count() > 0:
                for r in ratings:
                    c.user_rating[int(r.v_category.id)] = int(r.rating)


    expositions = category.exposition_set.all()
    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'parent_category': parent,
        'parent_categories': Category.objects.filter(parent=None),
        'selected_category': category,
        'vote_categories': VoteCategory.objects.all(),
    })
    return HttpResponse(t.render(c))

def index(request):
    """
    - Generates the home page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    
    # get the highest ranked submissions
    top_ranked_videos = cache.get('top_ranked_videos')
    if not top_ranked_videos:
        top_ranked_videos = []
        for category in VoteCategory.objects.all():
            # for now, calculate an average for each video
            top_ranked_videos.append({
                'vote_category': category, 
                'submissions': Submission.objects.filter(votes__v_category=category).annotate(average_rating=Avg('votes__rating')).order_by('-average_rating')[:5],
            })
        cache.set('top_ranked_videos', top_ranked_videos, 60*10)

    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
        'parent_categories': Category.objects.filter(parent=None),
        'top_ranked_videos': top_ranked_videos,
        'vote_categories': VoteCategory.objects.all(),
    })
    return HttpResponse(t.render(c))

def post(request, sid):
    """
    - Generates the view for the specific post (submission) from `sid`
    - Creates the appropriate breadcrumbs for the categories
    """
    s = Submission.objects.get(id=sid)
    s.video = [v for v in json.loads(s.video)]
    breadcrumbs = [{'url': reverse('home'), 'title': 'Home'}]

    parent_categories = s.tags.filter(parent=None)
    if len(parent_categories) >= 1:
        parent = parent_categories[0]
        breadcrumbs.append({'url': reverse('category', args=[parent.id]), 'title': parent})
    else: parent = None

    categories = s.tags.filter( ~Q(parent=None) )
    if len(categories) >= 1: 
        category = categories[0]
    else: category = None

    if parent == None:
        c = category.parent.all()
        if len(c) > 0:
            c = category.parent.all()[0]
            breadcrumbs.append({'url': reverse('category', args=[c.id]), 'title': c})
                
    if category:
        breadcrumbs.append({'url': reverse('category', args=[category.id]), 'title': category})

    t = loader.get_template('home/index.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': [s],
        'parent_category': parent,
        'parent_categories': Category.objects.filter(parent=None),
        'selected_category': category,
        'vote_categories': VoteCategory.objects.all(),
    })
    return HttpResponse(t.render(c))
