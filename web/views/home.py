from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404
import json
from web.models import *#Category, Submission, VoteCategory, Class, LectureNote
from itertools import chain

def index(request):
    template = loader.get_template('home/index.html')
    class_list = Class.objects.order_by('name')
    context = RequestContext(request, {'class_list': class_list,
    })
    return HttpResponse(template.render(context))

##def category(request, pk, cat):
##    """
##    - Generates the view for a specific category
##    - Creates the breadcrumbs for the page
##    """
##    current_class = get_object_or_404(Class, pk=pk)
##    #Get category we are in
##    category = get_object_or_404(Category.objects, id=cat)
##    categories_in_class = Category.objects.get(parent_class=current_class.id)
##    parents = category.parent.all()
##    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
##
##    if len(parents) == 0:
##        parent = category
##        content = Submission.objects.filter( Q(tags=category) | Q(tags__in=category.child.distinct()) ).distinct()
##    else:
##        parent = parents[0]
##        content = Submission.objects.filter( Q(tags=category) ).distinct()
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id, parent.id]), 'title': parent})
##
##    breadcrumbs.append({'url': reverse('category', args=[current_class.id, category.id]), 'title': category})
##
##    # un-json-fy the videos
##    for c in content:
##        if c.video: c.video = [v for v in json.loads(c.video)]
##
##    if request.user.is_authenticated():
##        for c in content:
##            ratings = c.votes.filter(user=request.user)
##            c.user_rating = {}
##            if ratings.count() > 0:
##                for r in ratings:
##                    c.user_rating[int(r.v_category.id)] = int(r.rating)
##    
##    #Selecting parents
##    child_categories = Category.objects.filter(class__id=pk).exclude(parent=None)
##    parent_categories = Category.objects.filter(Q(child__in=child_categories)|Q(parent=None, class__id=pk))
##    L = list()
##    for item in parent_categories:
##        if L.count(item) == 0:
##            L.append(item)
### print(L)
##
##    #Adding new parent_of_child_categories to current class
##    parent_of_child_categories = Category.objects.filter(child__in=child_categories).exclude(class__id=pk)
##    for z in parent_of_child_categories:
##        add_parent_to_class = current_class.categories.add(z)
##        current_class.save();
##        class_of_parent = z.class_set.all()
##        print(class_of_parent)
##
##    expositions = category.exposition_set.all()
##    lectureNotes = LectureNote.objects.filter(classBelong = current_class)
##    for e in lectureNotes:
##        print(e.file)
##    t = loader.get_template('home/classes.html')
##    c = RequestContext(request, {
##        'breadcrumbs': breadcrumbs,
##        'content': content,
##        'expositions': expositions,
##        'lectureNotes': lectureNotes,
##        'parent_category': parent,
##        'parent_categories': L,
##        'child_categories': child_categories,
##        'selected_category': category,
##        'vote_categories': VoteCategory.objects.all(),
##        'current_class':current_class,
##        'categories_in_class':categories_in_class,
##    })
##    return HttpResponse(t.render(c))
##

def category(request, class_id, cat_id):
    """
    - Generates the category page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    #get category we are in
    current_category = get_object_or_404(Category, id=cat_id)
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
    #Get list of parent categories
    parent_categories = list()
    parent_categories.append(current_category)
    tmp_categories = current_category.parent_categories.all()
    while tmp_categories:
        parent_categories.append(tmp_categories[0])
        print(tmp_categories[0])
        tmp_categories = tmp_categories[0].parent_categories.all()

    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('classes', args=[current_class.id]), 'title': parent_categories[-i]})
        
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


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'top_ranked_videos': top_ranked_videos,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
    })
    return HttpResponse(t.render(c))


def atom(request, class_id, cat_id, atom_id):
    """
    - Generates the view for a specific category
    - Creates the breadcrumbs for the page
    """
    #Get atom we are in
    current_atom = get_object_or_404(Atom, id=atom_id)
    #get category we are in
    current_category = get_object_or_404(Category, id=cat_id)
##    #Get the parents of the category we are in
##    parents = current_category.parent_categories.all() #Check that it is correct
    
    #Get class we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None) #check that this works

    #Get list of parent categories
    parent_categories = list()
    parent_categories.append(current_category)
    tmp_categories = current_category.parent_categories.filter(parent_class = current_class.id)
    while tmp_categories:
        parent_categories.append(tmp_categories[0])
        print(tmp_categories[0])
        tmp_categories = tmp_categories[0].parent_categories.filter(parent_class = current_class.id)
            
    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('classes', args=[current_class.id]), 'title': parent_categories[-i]})
    breadcrumbs.append({'url': reverse('atom', args=[current_class.id, current_category.id, current_atom.id]), 'title': current_atom})

    
    content = Submission.objects.filter( Q(tags=current_category) ).distinct()
##    if len(parents) == 0:
##        parent = current_category
##        content = Submission.objects.filter( Q(tags=current_category) | Q(tags__in=current_category.child_categories.distinct()) ).distinct()
##    else:
##        parent = parents[0]
##        content = Submission.objects.filter( Q(tags=current_category) ).distinct()
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id, parent.id]), 'title': parent})

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


    expositions = current_atom.exposition_set.all()
    lectureNotes = LectureNote.objects.filter(classBelong = current_class)


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': content,
        'expositions': expositions,
        'lectureNotes': lectureNotes,
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'selected_atom': current_atom,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
        'categories_in_class':categories_in_class,
    })
    return HttpResponse(t.render(c))


def classes(request, class_id):
    """
    - Generates the home page
    - Generates a list of the most popular videos for each category of rating
    - Use memcached to save the popular video rankings to save a lot of time
    """
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
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


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url':reverse('classes', args=[current_class.id]), 'title': current_class.name}],
        'top_level_categories': top_level_categories,
        'top_ranked_videos': top_ranked_videos,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
    })
    return HttpResponse(t.render(c))

def post(request, class_id, sid):
    """
    - Generates the view for the specific post (submission) from `sid`
    - Creates the appropriate breadcrumbs for the categories
    """
    #Get the class that we are in
    current_class = get_object_or_404(Class, id=class_id)
    #Get categories that are in the current_class
    categories_in_class = Category.objects.filter(parent_class=current_class.id)
    #Get the "top level" categories
    top_level_categories = categories_in_class.filter(parent_categories=None)
    
    s = Submission.objects.get(id=sid)
    
    if s.video:
        s.video = [v for v in json.loads(s.video)]

    current_atom = s.tags.all()[0]
    current_category = current_atom.category_set.filter(parent_class = current_class.id)[0]
    
    #Get list of parent categories
    parent_categories = list()
    parent_categories.append(current_category)
    tmp_categories = current_category.parent_categories.filter(parent_class = current_class.id)
    while tmp_categories:
        parent_categories.append(tmp_categories[0])
        print(tmp_categories[0])
        tmp_categories = tmp_categories[0].parent_categories.filter(parent_class = current_class.id)


    breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
    for i in range(1, len(parent_categories)+1):
        breadcrumbs.append({'url' : reverse('classes', args=[current_class.id]), 'title': parent_categories[-i]})
    breadcrumbs.append({'url': reverse('atom', args=[current_class.id, current_category.id, current_atom.id]), 'title': current_atom})
##    if len(parent_categories) >= 1:
##        parent = parent_categories[0]
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id,parent.id]), 'title': parent})
##    else: parent = None
##
##    categories = s.tags.filter( ~Q(parent=None) )
##    if len(categories) >= 1: 
##        category = categories[0]
##    else: category = None
##
##    if parent == None:
##        c = category.parent.all()
##        if len(c) > 0:
##            c = category.parent.all()[0]
##            breadcrumbs.append({'url': reverse('category', args=[current_class.id,c.id]), 'title': c})
##                
##    if category:
##        breadcrumbs.append({'url': reverse('category', args=[current_class.id,category.id]), 'title': category})


    t = loader.get_template('home/classes.html')
    c = RequestContext(request, {
        'breadcrumbs': breadcrumbs,
        'content': [s],
        'top_level_categories': top_level_categories,
        'selected_categories': parent_categories,
        'selected_atom': current_atom,
        'vote_categories': VoteCategory.objects.all(),
        'current_class':current_class,
    })
    return HttpResponse(t.render(c))