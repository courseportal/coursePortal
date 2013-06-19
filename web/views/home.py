from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.db.models.loading import get_models
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.shortcuts import get_object_or_404
import json

from pybb.models import Forum
from django.core.mail import send_mail, BadHeaderError
from web.forms.submission import testModalForm

for m in get_models():
	exec "from %s import %s" % (m.__module__, m.__name__)


def class_index(request):
	
	#Get the "top level" categories
	top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)
	class_list = Class.objects.all()
	
	template = loader.get_template('web/home/class_index.html')
	context = RequestContext(request, {
		'breadcrumbs': [{'url': reverse('class_index'), 'title': 'Class Index'}],
		'class_list': class_list,
		'top_level_categories': top_level_base_categories,
	})
	return HttpResponse(template.render(context))

def index(request):
	"""
	This is the home view for categories when you aren't in a class and haven't clicked on a category/atom yet.
	
	For now this displays the top ranked videos for all of the categories, we need to change it eventually.
	"""
	#Get the "top level" categories
	top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)

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
		
	template = loader.get_template('web/home/base/index.html')
	context = RequestContext(request, {
		'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}],
		'top_level_categories': top_level_base_categories,
		'top_ranked_videos': top_ranked_videos,
	})
	return HttpResponse(template.render(context))


def get_content_for_category(current_category, mode, content_list=[]):
	"""
	This function returns the content for a category. Set content_list=[].
	
	The mode variable determines what kind of data to return:
		*	mode = 0
				Return submission data
		*	mode = 1
				Return exposition data
		*	mode = 2
				Return lecture note data
		*	mode = 3
				Return example data
		*	else
				Return an empty list
	
	We define content "in this category" if the content belongs to an atom that is in ``current_category`` or any of its sub-categories.  To acchieve this we use recursion.
	
	.. warning::
	
		You have to input an empty list for content_list when calling this function.  The default argument doesn't work and causes both expositions and Submissions to be added to the same list.
	
	"""
	for atom in current_category.child_atoms.all():
		
			# Do something depending on what mode is set
		if mode == 0:
			content = Submission.objects.filter(tags = atom).distinct()
		elif mode == 1:
			content = atom.exposition_set.all()
		elif mode == 2:
			content = atom.lecturenote_set.all()
		elif mode == 3:
			content = atom.example_set.all()
		else:
			return []
			
		for c in content:
			if not content_list.count(c):
				content_list.append(c)
	for child in current_category.child_categories.all():
		get_content_for_category(current_category=child, mode=mode, content_list=content_list) #recurse
	return content_list

def get_parent_categories(current_category, current_class=None):
	"""
	This function gets all of the parent categories for ``current_category``.
	
	If ``current_class`` is not set then it will filter the parent_categories list to only include categories that are in ``current_class``, otherwise it will return all parent categories.
	
	.. warning::
		
		If there are loops in your categories this will result in infinite loops, but you shouldn't be able to create categories in the admin site that result in infinite loops.
	
	"""
	parent_categories=list()
	parent_categories.append(current_category)
	if current_class:
		tmp_categories = current_category.parent_categories.filter(parent_class=current_class.id)
	else:
		tmp_categories = current_category.parent_categories.all()
	while tmp_categories:
		parent_categories.append(tmp_categories[0])
		if current_class:
			tmp_categories = tmp_categories[0].parent_categories.filter(parent_class = current_class.id)
		else:
			tmp_categories = tmp_categories[0].parent_categories.all()
	return parent_categories


def findChildAtom(current_category, atom_list):
	for c_a in current_category.child_atoms.all():
		atom_list.append(c_a)
	for c_c in current_category.child_categories.all():
		for c in c_c.child_atoms.all():
			atom_list.append(c)
		current_category=c_c.child_categories.all()
		if current_category:
			for a in current_category.all():
				findChildAtom(a, atom_list)
	return atom_list


def base_category(request, cat_id):
	"""
		-	Generates the category page
		-	Generates a list of the most popular videos for each category of rating
		-	Use memcached to save the popular video rankings to save a lot of time
	"""
	
	if request.method == 'POST': # If the form has been submitted...
		form = testModalForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('base_category', args=(cat_id,))) 
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = testModalForm()
	
	#get category we are in
	current_category = get_object_or_404(BaseCategory, id=cat_id)
	#Get the "top level" categories
	top_level_base_categories = BaseCategory.objects.filter(parent_categories=None)
	
	parent_categories = get_parent_categories(current_category=current_category)

	#Setting breadcrumbs, not perfect, improvements can be made
	breadcrumbs = []
	for i in range(1, len(parent_categories)+1):
		breadcrumbs.append({'url' : reverse('base_category', args=[parent_categories[-i].id]), 'title': parent_categories[-i]})

	#Get collection of videos from all atoms in this category or sub-categories
	content = get_content_for_category(current_category=current_category, mode=0, content_list=[])
	expositions = get_content_for_category(current_category=current_category, mode=1, content_list=[])
	notes = get_content_for_category(current_category=current_category, mode=2, content_list=[])
	examples = get_content_for_category(current_category=current_category, mode=3, content_list=[])
	
	
	# un-json-fy the videos
	for c in content:
		if c.video: c.video = [v for v in json.loads(c.video)]

	if request.user.is_authenticated():
		for c in content:
			ratings = c.votes_s.filter(user=request.user)
			c.user_rating = {}
			if ratings.count() > 0:
				for r in ratings:
					c.user_rating[int(r.v_category.id)] = int(r.rating)
	#get all the atoms in and under the current category
	atom_list = list()
	temp_atom_list = findChildAtom(current_category,list())
	for item in temp_atom_list:
		if atom_list.count(item)==0:
			atom_list.append(item)
	length = int(len(atom_list))/3+1
	list_1 = atom_list[0:length]
	list_2 = atom_list[length:length*2]
	list_3 = atom_list[length*2:]

	t = loader.get_template('web/home/base/category.html')
	c = RequestContext(request, {
		'breadcrumbs': breadcrumbs,
		'content': content,
		'expositions': expositions,
		#'lectureNotes': lectureNotes,
		'top_level_categories': top_level_base_categories,
		'selected_categories': parent_categories,
		#'selected_category': current_category,
		'atom_list_1': list_1,
		'atom_list_2': list_2,
		'atom_list_3': list_3,
		'vote_categories': VoteCategory.objects.all(),
		'notes': notes,
		'examples': examples,
		'form': form,
	})
	return HttpResponse(t.render(c))

def base_atom(request, cat_id, atom_id):

	"""
		- Generates the view for a specific category
		- Creates the breadcrumbs for the page
		"""
	if request.method == 'POST': # If the form has been submitted...
		form = testModalForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('base_category', args=(cat_id,))) 
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = testModalForm()

	#Get atom we are in
	current_atom = get_object_or_404(Atom, id=atom_id)
	#get category we are in
	current_category = get_object_or_404(BaseCategory, id=cat_id)
	#Get the "top level" categories
	top_level_base_categories = BaseCategory.objects.filter(parent_categories=None) #check that this works

	parent_categories = get_parent_categories(current_category=current_category)

	breadcrumbs = []
	for i in range(1, len(parent_categories)+1):
		breadcrumbs.append({'url' : reverse('base_category', args=[parent_categories[-i].id]), 'title': parent_categories[-i]})
	breadcrumbs.append({'url': reverse('base_atom', args=[current_category.id, current_atom.id]), 'title': current_atom})

	
	content = Submission.objects.filter(tags=current_atom).distinct()
	
	forum = Forum.objects.get(atom=current_atom)


	# un-json-fy the videos
	for c in content:
		if c.video: c.video = [v for v in json.loads(c.video)]

	if request.user.is_authenticated():
		for c in content:
			ratings = c.votes_s.filter(user=request.user)
			c.user_rating = {}
			if ratings.count() > 0:
				for r in ratings:
					c.user_rating[int(r.v_category.id)] = int(r.rating)


	expositions = current_atom.exposition_set.all()
	notes = current_atom.lecturenote_set.all()
	examples = current_atom.example_set.all()


	t = loader.get_template('web/home/base/atom.html')
	c = RequestContext(request, {
		'breadcrumbs': breadcrumbs,
		'content': content,
		'expositions': expositions,
		'top_level_categories': top_level_base_categories,
		'selected_categories': parent_categories,
		#'selected_category': current_category,
		'selected_atom': current_atom,
		'vote_categories': VoteCategory.objects.all(),
		'forum': forum,
		'notes': notes,
		'examples': examples,
		'form': form,
	})
	return HttpResponse(t.render(c))
	

def category(request, class_id, cat_id):
	"""
		- Generates the category page
		- Generates a list of the most popular videos for each category of rating
		- Use memcached to save the popular video rankings to save a lot of time
		"""
	if request.method == 'POST': # If the form has been submitted...
		form = testModalForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('base_category', args=(cat_id,))) 
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = testModalForm()
	
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
		
		'stickied_content': stickied_content,
		'stickied_expositions': stickied_expositions,
		'stickied_notes': stickied_notes,
		'stickied_examples': stickied_examples,
		'content': content,
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
		form = testModalForm(request.POST)
		if form.is_valid():	# All validation rules pass
			subject = "[Community Guideline Violation Report]:  " + form.cleaned_data['subject']
			content = "From \"" + request.user.username + "\" : \n\nCommunity Guideline Violation Report:\t\t" + form.cleaned_data['content'] + "\n\nContent Type:\t\t" + request.POST.get('contentType')+"\n\nContent Id:\t\t "+request.POST.get('contentId')
			send_mail(subject, content,'test-no-use@umich.edu', ['knoatom.webmaster@gmail.com'])
			messages.warning(request, 'Report has been successfully submitted. Thank you!')
			return HttpResponseRedirect(reverse('base_category', args=(cat_id,))) 
		else:
			messages.warning(request, 'Error saving. Fields might be invalid.')
	else:
		form = testModalForm()
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
		
		'stickied_content': stickied_content,
		'stickied_expositions': stickied_expositions,
		'stickied_notes': stickied_notes,
		'stickied_examples': stickied_examples,
		'content': content,
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




def bugReportConfirm(request, bid):
	b = BugReport.objects.get(id=bid)
	subject = b.subject
	content = b.content
	email= b.email
	t = loader.get_template('web/home/confirm.html')
	c = RequestContext(request, {
					   'subject': subject,
					   'content': content,
					   'email': email,
					   })
	return HttpResponse(t.render(c))
