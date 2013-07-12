from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.db.models.loading import get_models
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404, render
import json

from pybb.models import Forum
from django.core.mail import send_mail
from web.forms.submission import ReportForm
from django.forms.util import ErrorList
from knoatom.view_functions import get_breadcrumbs, render_to_json_response # Site wide helper fn's
from web.views.view_functions import get_navbar_context, get_context_for_category, web_breadcrumb_dict

for m in get_models():
	exec "from %s import %s" % (m.__module__, m.__name__)
	
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
			context.update(form.errors) # Add the errors to the context to be processed by AJAX
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
	context = get_navbar_context() # Add the initial navbar content.  There are no breadcrumbs
	
	# get the highest ranked submissions
	top_ranked_videos = cache.get('top_ranked_videos') # Try to load the videos from the cache
	if not top_ranked_videos: # If there is no cached version
		top_ranked_videos = Submission.objects.all().order_by('-votes')[:5] # Query for top 5 videos
		cache.set('top_ranked_videos', top_ranked_videos, 60*10) # Set cache to last for 10 mins
	context.update({
		'top_ranked_videos': top_ranked_videos,
	})
	
	return render(request, 'web/home/base/index.html', context)

def base_category(request, pk):
	"""
		-	Generates the category page
		-	Generates a list of the most popular videos for each category of rating
		-	Use memcached to save the popular video rankings to save a lot of time
	"""
	category_object = get_object_or_404(BaseCategory, id=pk)
	# Get the navbar context as the initial context, ('top_level_categories', 'selected_categories')
	context = get_navbar_context(category_object)
	context.update({
		'selected_category':category_object
	})
	context.update( # Adds 'breadcrumbs' to context
		get_breadcrumbs(request.path, web_breadcrumb_dict)
	)
	#Get collection of videos/expos/notes/examples from all atoms in this category or sub-categories
	context.update( # And a list of all sub-atoms (including atoms in sub-categories)
		get_context_for_category(category_object)
	)
	##################################################################################################
	# un-json-fy the videos					### Do we want to be able to save multiple videos?
	for c in context['videos']:
		if c.video: 
			c.video = [v for v in json.loads(c.video)]
	##################################################################################################
	return render(request, 'web/home/base/category.html', context)

def base_atom(request, cat_id, atom_id):
	"""
		- Generates the view for a specific category
		- Creates the breadcrumbs for the page
	"""
	category_object = get_object_or_404(BaseCategory, id=cat_id) # Get category we are in
	atom_object = get_object_or_404(Atom, id=atom_id) # Get atom we are in
	
	context = get_navbar_context(category_object) #'top_level_base_categories, 'selected_categories'
	context.update( # Adds 'breadcrumbs' to the context.
		get_breadcrumbs(request.path, web_breadcrumb_dict)
	)
	context.update({ # Get the contents of the atom and add them to the context dict
	'selected_atom':atom_object,
	'videos':		Submission.objects.filter(tags=atom_object).distinct(),
	'expositions':	atom_object.exposition_set.all(),
	'notes':		atom_object.lecturenote_set.all(),
	'examples':		atom_object.example_set.all(),
	'forum':		Forum.objects.get(atom=atom_object),
	})
	##################################################################################################
	# un-json-fy the videos					### Do we want to be able to save multiple videos?
	for c in context['videos']:
		if c.video: 
			c.video = [v for v in json.loads(c.video)]
	##################################################################################################
	return render(request, 'web/home/base/atom.html', context)
	

def category(request, class_id, cat_id):
	"""
		- Generates the category page
		- Generates a list of the most popular videos for each category of rating
		- Use memcached to save the popular video rankings to save a lot of time
	"""
	if request.method == 'POST': # If the form has been submitted...
	#print(request.POST.get('contentType'))
		form = ReportForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('category', args=(class_id, cat_id)))
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = ReportForm()
	
	#get category we are in
	current_category = get_object_or_404(AtomCategory, id=cat_id)
	#Get the class that we are in
	current_class = get_object_or_404(Class, id=class_id)
	#Get categories that are in the current_class
	categories_in_class = AtomCategory.objects.filter(parent_class=current_class.id)
	#Get the "top level" categories
	top_level_categories = categories_in_class.filter(parent_categories=None)
	
	parent_categories = get_parent_categories(current_category=current_category, current_class=current_class)

	#Setting breadcrumbs, not perfect, improvements can be made
	breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
	for i in range(1, len(parent_categories)+1):
		breadcrumbs.append({'url' : reverse('category', args=[current_class.id, parent_categories[-i].id]), 'title': parent_categories[-i]})

	#Get collection of videos from all atoms in this category or sub-categories
	all_content = get_content_for_category(current_category=current_category, mode=0, content_list=[])
	all_expositions = get_content_for_category(current_category=current_category, mode=1, content_list=[])
	all_notes = get_content_for_category(current_category=current_category, mode=2, content_list=[])
	all_examples = get_content_for_category(current_category=current_category, mode=3, content_list=[])
			
	
			
	
	# un-json-fy the videos
	for c in all_content:
		if c.video: c.video = [v for v in json.loads(c.video)]

		if request.user.is_authenticated():
			for c in all_content:
				ratings = c.votes_s.filter(user=request.user)
				c.user_rating = {}
				if ratings.count() > 0:
					for r in ratings:
						c.user_rating[int(r.v_category.id)] = int(r.rating)
					
					
	stickied_content = []
	content = []
	for vid in all_content:
		if vid.classes_stickied_in.filter(id=current_class.id).exists():
			stickied_content.append(vid)
		else:
			content.append(vid)
					
	stickied_expositions = []
	expositions = []
	for expo in all_expositions:
		if expo.classes_stickied_in.filter(id=current_class.id).exists():
			stickied_expositions.append(expo)
		else:
			expositions.append(expo)
			
	stickied_notes = []
	notes = []
	for note in all_notes:
		if note.classes_stickied_in.filter(id=current_class.id).exists():
			stickied_notes.append(note)
		else:
			notes.append(note)
			
	stickied_examples = []
	examples = []
	for example in all_examples:
		if example.classes_stickied_in.filter(id=current_class.id).exists():
			stickied_examples.append(example)
		else:
			examples.append(example)

	#get all the atoms in and under the current category
	atom_list = list()
	temp_atom_list = findChildAtom(current_category,list())
	for item in temp_atom_list:
		if atom_list.count(item)==0:
			atom_list.append(item)
	length = len(atom_list)/3+1
	list_1 = atom_list[0:length]
	list_2 = atom_list[length:length*2]
	list_3 = atom_list[length*2:]

	t = loader.get_template('web/home/class/category.html')
	c = RequestContext(request, {
		'breadcrumbs': breadcrumbs,
		'top_level_categories': top_level_categories,
		'selected_categories': parent_categories,
		'atom_list_1': list_1,
		'atom_list_2': list_2,
		'atom_list_3': list_3,
		'vote_categories': VoteCategory.objects.all(),
		'selected_class':current_class,
		
		'stickied_videos': stickied_content,
		'stickied_expositions': stickied_expositions,
		'stickied_notes': stickied_notes,
		'stickied_examples': stickied_examples,
		'videos': content,
		'expositions': expositions,
		'notes': notes,
		'examples': examples,
		'form': form,
	})
	return HttpResponse(t.render(c))


def atom(request, class_id, cat_id, atom_id):
	"""
		- Generates the view for a specific category
		- Creates the breadcrumbs for the page
	"""
	if request.method == 'POST': # If the form has been submitted...
		form = ReportForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('atom', args=(class_id, cat_id, atom_id)))
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = ReportForm()


	#Get atom we are in
	current_atom = get_object_or_404(Atom, id=atom_id)
	#get category we are in
	current_category = get_object_or_404(AtomCategory, id=cat_id)
##	#Get the parents of the category we are in
##	parents = current_category.parent_categories.all() #Check that it is correct
	
	#Get class we are in
	current_class = get_object_or_404(Class, id=class_id)
	#Get categories that are in the current_class
	categories_in_class = AtomCategory.objects.filter(parent_class=current_class.id)
	#Get the "top level" categories
	top_level_categories = categories_in_class.filter(parent_categories=None) #check that this works

	#Get list of parent categories, not perfect, improvements can be made
	parent_categories = get_parent_categories(current_category=current_category, current_class=current_class)


	breadcrumbs = [{'url': reverse('classes', args=[current_class.id]), 'title': current_class.name}]
	for i in range(1, len(parent_categories)+1):
		breadcrumbs.append({'url' : reverse('category', args=[current_class.id, parent_categories[-i].id]), 'title': parent_categories[-i]})
	breadcrumbs.append({'url': reverse('atom', args=[current_class.id, current_category.id, current_atom.id]), 'title': current_atom})

	forum = Forum.objects.get(atom=current_atom)
	
	all_content = Submission.objects.filter( Q(tags=current_atom) ).distinct()
	
	# un-json-fy the videos
	for c in all_content:
		if c.video: c.video = [v for v in json.loads(c.video)]

	if request.user.is_authenticated():
		
		for c in all_content:
			ratings = c.votes_s.filter(user=request.user)
			c.user_rating = {}
			if ratings.count() > 0:
				for r in ratings:
					c.user_rating[int(r.v_category.id)] = int(r.rating)

	stickied_content = []
	content = []
	for vid in all_content:
		if vid.classes_stickied_in.filter(id=current_class.id).exists():
			stickied_content.append(vid)
		else:
			content.append(vid)
	
	stickied_expositions = current_class.stickied_expos.filter(atom=current_atom)
	expositions = current_atom.exposition_set.exclude(id__in = stickied_expositions)
	
	stickied_notes = current_class.stickied_notes.filter(atom=current_atom)
	notes = current_atom.lecturenote_set.exclude(id__in = stickied_notes)
	
	stickied_examples = current_class.stickied_examples.filter(atom=current_atom)
	examples = current_atom.example_set.exclude(id__in = stickied_examples)

	t = loader.get_template('web/home/class/category.html')
	c = RequestContext(request, {
		'breadcrumbs': breadcrumbs,
		'top_level_categories': top_level_categories,
		'selected_categories': parent_categories,
		#'selected_category': current_category,
		'selected_atom': current_atom,
		'vote_categories': VoteCategory.objects.all(),
		'selected_class':current_class,
		'forum': forum,
		
		'stickied_videos': stickied_content,
		'stickied_expositions': stickied_expositions,
		'stickied_notes': stickied_notes,
		'stickied_examples': stickied_examples,
		'videos': content,
		'expositions': expositions,
		'notes': notes,
		'examples': examples,
		'form': form,
	})
	return HttpResponse(t.render(c))


def classes(request, class_id):
	"""
		-	Generates the home page
		-	Generates a list of the most popular videos for each category of rating
		-	Use memcached to save the popular video rankings to save a lot of time
	"""
		
	#Get the class that we are in
	current_class = get_object_or_404(Class, id=class_id)
	
	if current_class.status == "N" and not (request.user.is_superuser or current_class.author == request.user or current_class.allowed_users.filter(id=request.user.id).exists()):
		return HttpResponseRedirect(reverse('class_index'))
	
	#Get categories that are in the current_class
	categories_in_class = AtomCategory.objects.filter(parent_class=current_class.id)
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


	t = loader.get_template('web/home/class/index.html')
	c = RequestContext(request, {
		'object': current_class,
		'breadcrumbs': [{'url':reverse('classes', args=[current_class.id]), 'title': current_class.name}],
		'top_level_categories': top_level_categories,
		'top_ranked_videos': top_ranked_videos,
		'vote_categories': VoteCategory.objects.all(),
		'selected_class':current_class,
	})
	return HttpResponse(t.render(c))

def post(request, sid):
	"""
	-	Generates the view for the specific post (submission) from `sid`
	-	Creates the appropriate breadcrumbs for the categories
	"""
	#Get the "top level" categories
	top_level_categories = BaseCategory.objects.filter(parent_categories=None)
	
	s = Submission.objects.get(id=sid)
	
	if s.video:
		s.video = [v for v in json.loads(s.video)]

	current_atom = s.tags.all()[0]
	current_category = current_atom.base_category
	
	parent_categories = get_parent_categories(current_category=current_category)
	breadcrumbs = []
	breadcrumbs.append({'url' : reverse('post', args=[s.id]), 'title': s})

	t = loader.get_template('web/home/post.html')
	c = RequestContext(request, {
		'breadcrumbs': breadcrumbs,
		'content': [s],
		'top_level_categories': top_level_categories,
		'selected_categories': parent_categories,
		#'selected_category': current_category,
		'selected_atom': current_atom,
		'vote_categories': VoteCategory.objects.all(),
	})
	return HttpResponse(t.render(c))