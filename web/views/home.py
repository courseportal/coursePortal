import json

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.db.models import Count

from pybb.models import Forum
from web.models import BaseCategory, Atom, Content, Class, ClassCategory
from web.forms.submission import ReportForm
from knoatom.view_functions import get_breadcrumbs, render_to_json_response
from web.views.view_functions import get_navbar_context, \
get_context_for_category, web_breadcrumb_dict, get_parent_categories, \
get_context_for_atom, has_class_access
    
def report(request):
    r"""View for processing the report form. It only accepts AJAX requests."""
    context = {}
    if not request.is_ajax():
        return HttpResponseBadRequest()
    if request.method == 'POST':
        form = ReportForm(request.POST) # Bind the form
        if form.is_valid():
            form.submit(request.user)
            context.update({    # Add the success message to the context
                'success': True,
            })
        else:
            context.update(form.errors) # Add errors to be processed by AJAX
        return render_to_json_response(context)
    else:
        return HttpResponseBadRequest()

def class_list(request):    
    r"""This is the view for the class list."""
    context = get_navbar_context()
    context.update(
        get_breadcrumbs(request.path, web_breadcrumb_dict) 
    )
    context.update({
        'class_list':    Class.objects.all()
    })
    return render(request, 'web/home/class_list.html', context)

def index(request):
    """
        This is the home view for categories when you aren't in a class and haven't clicked on a category/atom yet.
    
        For now this displays the top ranked videos for all of the categories, we need to change it eventually.
    """
    context = get_navbar_context() # Add the initial navbar content.
    # top_ranked_videos = cache.get('top_ranked_videos') # Load from cache
#     if top_ranked_videos is None: # If there is no cached version
#         top_ranked_videos = Video.objects.all().annotate(votes=Count('vote')).order_by('-votes')[:5]
#         cache.set('top_ranked_videos', top_ranked_videos, 60*10) # Set cache
#     context.update({ # Add 'top_ranked_videos' to context
#         'top_ranked_videos': top_ranked_videos,
#     })
    return render(request, 'web/home/base/index.html', context)    

def category(request, cat_id, class_id=None):
    r"""
    This is the view for category and base_category (``/class/<class_id>/category/<cat_id>`` and ``/category/<cat_id>``).  It generates the category page which has a table of all the content in all of its ``child_atoms`` and all of the ``child_atoms`` in all categories under it.
    """
    if class_id is not None:
        template = 'web/content_list.html'
        category_object = get_object_or_404(ClassCategory, id=cat_id)
        class_object = get_object_or_404(Class, id=class_id)
        # Check if user is allowed to see this page
        if has_class_access(class_object, request.user):
            return HttpResponseRedirect(reverse('class_index')) # Redirect
    else:
        template = 'web/content_list.html'
        category_object = get_object_or_404(BaseCategory, id=cat_id)
        class_object = None # We aren't in a class
    context = get_navbar_context(category_object, class_object)
    
    context.update( # Add the breadrumbs to the context
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    print(get_context_for_category(category_object))
    context.update( # Add the category specific content to the context
        get_context_for_category(category_object)
    )
    context.update({
        'content_types':Content.CONTENT_TYPES,
        'title':category_object.title,
        'class_object':class_object,
        'category_object':category_object,
    })
    return render(request, template, context)
    


def atom(request, cat_id, atom_id, class_id=None):
    r"""
    This is the view for both the ``atom`` view and the ``base_atom`` view (``/class/<class_id>/category/<cat_id>/atom/<atom_id>`` and ``/category/<cat_id>/atom/<atom_id>``).  It generates the content that is contained in the atom.
    """
    if class_id is not None:
        template = 'web/content_list.html'
        class_object = get_object_or_404(Class, id=class_id)
        category_object = get_object_or_404(ClassCategory, id=cat_id)
        # Check if user is allowed to see this page
        if has_class_access(class_object, request.user):
            return HttpResponseRedirect(reverse('class_index')) # Redirect
    else:
        template = 'web/content_list.html'
        class_object = None
        category_object = get_object_or_404(BaseCategory, id=cat_id)
    atom_object = get_object_or_404(Atom, id=atom_id) 
    context = get_navbar_context(category_object, class_object)
    context.update( # Add the breadcrumbs to the context
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    print(get_context_for_atom(atom_object))
    context.update( # Add the atom specific content to the context
        get_context_for_atom(atom_object)
    )
    context.update({
        'content_types':Content.CONTENT_TYPES,
        'title': atom_object.title,
        'atom_object': atom_object,
        'category_object': category_object,
        'class_object':class_object,
        'forum': Forum.objects.get(atom=atom_object),
    })
    return render(request, template, context)

def content_detail(request, pk):
    r"""
    This is the view for the content detail view page.
    """
    # Custom breadcrumbs using GET data
    class_pk = request.GET.get('class', None)
    category_pk = request.GET.get('category', None)
    atom_pk = request.GET.get('atom', None)
    breadcrumbs = []
    class_ = cat = atom = None # Set them all to None
    if class_pk is not None:
        class_ = get_object_or_404(Class, pk=class_pk)
        breadcrumbs.append({'title':class_.title, 'url':reverse('classes', 
            args=[class_.pk])})
    if category_pk is not None:
        if class_pk is not None:
            cat = get_object_or_404(ClassCategory, pk=category_pk)
            breadcrumbs.append({'title':cat.title, 'url':reverse('category', 
                args=[class_.pk, cat.pk])})
        else:
            cat = get_object_or_404(BaseCategory, pk=category_pk)
            breadcrumbs.append({'title':cat.title, 
                'url':reverse('base_category', args=[cat.pk])})
    if atom_pk is not None:
        atom = get_object_or_404(Atom, pk=atom_pk)
        if class_pk is not None:
            breadcrumbs.append({'title':atom.title, 'url':reverse('atom', 
                args=[class_.pk, cat.pk, atom.pk])})
        else:
            breadcrumbs.append({'title':atom.title, 'url':reverse('base_atom', 
                args=[cat.pk, atom.pk])})
    # End custom breadcrumbs
    
    obj = get_object_or_404(Content, pk=pk)
    breadcrumbs.append({'title':"{} Details".format(obj.title), 
        'url':obj.get_absolute_url(class_, cat, atom)})
    context = get_navbar_context(cat, class_)
    context.update({
        'atom_object':atom,
        'category_object':cat,
        'class_object':class_,
        'content_object':obj,
        'breadcrumbs':breadcrumbs,
    })
    return render(request, 'web/content_details.html', context)

def classes(request, class_id):
    r"""
    This is the view for the class home page.  It shows the class summary.
    """
    class_object = get_object_or_404(Class, id=class_id)
    # Check if user is allowed to see this page
    if has_class_access(class_object, request.user):
        return HttpResponseRedirect(reverse('class_index')) # If not redirect
    context = get_navbar_context(None, class_object)
    context.update( # Add breadcrumbs to context
        get_breadcrumbs(request.path, web_breadcrumb_dict)
    )
    context.update({ # Add the class_objet to the context
        'class_object': class_object
    })
    return render(request, 'web/home/class/index.html', context)