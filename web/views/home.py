import json

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render

from pybb.models import Forum
from web.models import BaseCategory, Atom, Submission, Exposition, \
LectureNote, Example, Class, AtomCategory
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
			context.update({	# Add the success message to the context
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
		'class_list':	Class.objects.all()
	})
	return render(request, 'web/home/class_list.html', context)

def index(request):
	"""
		This is the home view for categories when you aren't in a class and haven't clicked on a category/atom yet.
	
		For now this displays the top ranked videos for all of the categories, we need to change it eventually.
	"""
	context = get_navbar_context() # Add the initial navbar content.
	top_ranked_videos = cache.get('top_ranked_videos') # Load from cache
	if not top_ranked_videos: # If there is no cached version
		top_ranked_videos = Submission.objects.all().order_by('-votes')[:5]
		cache.set('top_ranked_videos', top_ranked_videos, 60*10) # Set cache
	context.update({ # Add 'top_ranked_videos' to context
		'top_ranked_videos': top_ranked_videos,
	})
	return render(request, 'web/home/base/index.html', context)	

def category(request, cat_id, class_id=None):
	r"""
		- Generates the category page
		- Generates a list of the most popular videos for each category of rating
		- Use memcached to save the popular video rankings to save a lot of time
	"""
	if class_id:
		template = 'web/home/class/category.html'
		category_object = get_object_or_404(AtomCategory, id=cat_id)
		class_object = get_object_or_404(Class, id=class_id)
		# Check if user is allowed to see this page
		if has_class_access(class_object, request.user):
			return HttpResponseRedirect(reverse('class_index')) # Redirect
	else:
		template = 'web/home/base/category.html'
		category_object = get_object_or_404(BaseCategory, id=cat_id)
		class_object = None # We aren't in a class
	context = get_navbar_context(category_object, class_object)
	context.update( # Add the breadrumbs to the context
		get_breadcrumbs(request.path, web_breadcrumb_dict)
	)
	context.update( # Add the category specific content to the context
		get_context_for_category(category_object)
	)
	# un-json-fy the videos
	for c in context['videos']:
		if c.video: c.video = [v for v in json.loads(c.video)]
	context.update({
		'selected_class':class_object,
		'selected_category':category_object,
	})

	return render(request, template, context)
	


def atom(request, cat_id, atom_id, class_id=None):
	r"""
		- Generates the view for a specific category
		- Creates the breadcrumbs for the page
	"""
	if class_id:
		template = 'web/home/class/category.html'
		class_object = get_object_or_404(Class, id=class_id)
		category_object = get_object_or_404(AtomCategory, id=cat_id)
		# Check if user is allowed to see this page
		if has_class_access(class_object, request.user):
			return HttpResponseRedirect(reverse('class_index')) # Redirect
	else:
		template = 'web/home/base/category.html'
		class_object = None
		category_object = get_object_or_404(BaseCategory, id=cat_id)
	atom_object = get_object_or_404(Atom, id=atom_id) 
	context = get_navbar_context(category_object, class_object)
	context.update( # Add the breadcrumbs to the context
		get_breadcrumbs(request.path, web_breadcrumb_dict)
	)
	context.update( # Add the atom specific content to the context
		get_context_for_atom(atom_object)
	)
	# un-json-fy the videos
	for c in context['videos']:
		if c.video: c.video = [v for v in json.loads(c.video)]

	context.update({
		'selected_atom': atom_object,
		'selected_class':class_object,
		'forum': Forum.objects.get(atom=atom_object),
	})
	return render(request, template, context)

def classes(request, class_id):
	"""
		-	Generates the home page
		-	Generates a list of the most popular videos for each category of rating
		-	Use memcached to save the popular video rankings to save a lot of time
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
		'selected_class': class_object
	})
	return render(request, 'web/home/class/index.html', context)

# def post(request, sid):
# 	"""
# 	-	Generates the view for the specific post (submission) from `sid`
# 	-	Creates the appropriate breadcrumbs for the categories
# 	"""
# 	#Get the "top level" categories
# 	top_level_categories = BaseCategory.objects.filter(parent_categories=None)
# 	
# 	s = Submission.objects.get(id=sid)
# 	
# 	if s.video:
# 		s.video = [v for v in json.loads(s.video)]
# 
# 	current_atom = s.tags.all()[0]
# 	current_category = current_atom.base_category
# 	
# 	context = get_parent_categories(current_category=current_category,current_class=None)
# 	breadcrumbs = []
# 	breadcrumbs.append({'url' : reverse('post', args=[s.id]), 'title': s})
# 
# 	t = loader.get_template('web/home/post.html')
# 	c = RequestContext(request, context.update({
# 		'breadcrumbs': breadcrumbs,
# 		'content': [s],
# 		'top_level_categories': top_level_categories,
# 		'selected_categories': parent_categories,
# 		#'selected_category': current_category,
# 		'selected_atom': current_atom,
# 		'vote_categories': VoteCategory.objects.all(),
# 	}))
# 	return HttpResponse(t.render(c))