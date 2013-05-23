from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404
import json
from web.models import Category, Submission, VoteCategory, Class
from itertools import chain

def index(request):
    template = loader.get_template('home/index.html')
    class_list = Class.objects.order_by('-name')
    context = RequestContext(request, {'class_list': class_list,
    })
    return HttpResponse(template.render(context))

def category(request, pk, cat):
    """
    - Generates the view for a specific category
    - Creates the breadcrumbs for the page
    """
    class_id = get_object_or_404(Class, pk=pk)
    
    category = get_object_or_404(class_id.categories, id=cat)
    categories_in_class = class_id.categories.all()
    
    parents = category.parent.all()
    breadcrumbs = [{'url': reverse('classes', args=[class_id.id]), 'title': class_id.name}]

    if len(parents) == 0:
        parent = category
        content = Submission.objects.filter( Q(tags=category) | Q(tags__in=category.child.distinct()) ).distinct()
    else:
        parent = parents[0]
        content = Submission.objects.filter( Q(tags=category) ).distinct()
        breadcrumbs.append({'url': reverse('category', args=[class_id.id, parent.id]), 'title': parent})

    breadcrumbs.append({'url': reverse('category', args=[class_id.id, category.id]), 'title': category})

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
    
    #Selecting parents
    child_categories = Category.objects.filter(class__id=pk).exclude(parent=None)
    parent_categories = Category.objects.filter(Q(child__in=child_categories)|Q(parent=None, class__id=pk))
    L = list()
    for item in parent_categories:
        if L.count(item) == 0:
            L.append(item)
# print(L)

    #Adding new parent_of_child_categories to current class
    parent_of_child_categories = Category.objects.filter(child__in=child_categories).exclude(class__id=pk)
    for z in parent_of_child_categories:
        add_parent_to_class = class_id.categories.add(z)
        class_id.save();
        class_of_parent = z.class_set.all()
        print(class_of_parent)

    expositions = category.exposition_set.all()
    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'parent_category': parent,
        'parent_categories': L,
        'child_categories': child_categories,
        'selected_category': category,
        'vote_categories': VoteCategory.objects.all(),
        'class_id':class_id,
        'categories_in_class':categories_in_class,
    })
    return HttpResponse(t.render(c))


def classes(request, pk):
    """
    - Generates the home page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    class_id = get_object_or_404(Class, pk=pk)
    
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

    #Selecting parents
    child_categories = Category.objects.filter(class__id=pk).exclude(parent=None)
    parent_categories = Category.objects.filter(Q(child__in=child_categories)|Q(parent=None, class__id=pk))
    L = list()
    for item in parent_categories:
        if L.count(item) == 0:
            L.append(item)
#print(L)

    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url':reverse('classes', args=[class_id.id]), 'title': class_id.name}],
        'parent_categories': L,
        'child_categories': child_categories,
        'top_ranked_videos': top_ranked_videos,
        'vote_categories': VoteCategory.objects.all(),
        'class_id':class_id,
    })
    return HttpResponse(t.render(c))

def post(request, pk, sid):
    """
    - Generates the view for the specific post (submission) from `sid`
    - Creates the appropriate breadcrumbs for the categories
    """
    class_id = get_object_or_404(Class, pk=pk)
    s = Submission.objects.get(id=sid)
    print(s.video)
    if s.video:
        s.video = [v for v in json.loads(s.video)]
    breadcrumbs = [{'url': reverse('classes', args=[class_id.id]), 'title': class_id.name}]
    parent_categories = s.tags.filter(parent=None)
    if len(parent_categories) >= 1:
        parent = parent_categories[0]
        breadcrumbs.append({'url': reverse('category', args=[class_id.id,parent.id]), 'title': parent})
    else: parent = None

    categories = s.tags.filter( ~Q(parent=None) )
    if len(categories) >= 1: 
        category = categories[0]
    else: category = None

    if parent == None:
        c = category.parent.all()
        if len(c) > 0:
            c = category.parent.all()[0]
            breadcrumbs.append({'url': reverse('category', args=[class_id.id,c.id]), 'title': c})
                
    if category:
        breadcrumbs.append({'url': reverse('category', args=[class_id.id,category.id]), 'title': category})

    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': [s],
        'parent_category': parent,
        'parent_categories': Category.objects.filter(parent=None),
        'selected_category': category,
        'vote_categories': VoteCategory.objects.all(),
        'class_id':class_id,
    })
    return HttpResponse(t.render(c))
