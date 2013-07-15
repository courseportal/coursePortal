r"""View helper functions."""
from itertools import chain
from django.shortcuts import get_object_or_404
from web.models import Class, AtomCategory, BaseCategory, Atom, Submission, Example, Exposition, LectureNote

# Dict to pass to the breadcrumb function to work with all of web.
web_breadcrumb_dict = {
	'class-index':	lambda pks: 'Class List',
	'class':		lambda pks: get_object_or_404(Class, pk=pks[0]),
	'category':		lambda pks: get_object_or_404(AtomCategory, pk=pks[0]),
	'atom':			lambda pks: get_object_or_404(Atom, pk=pks[0]),
}

def get_navbar_context(category_object=None, class_object=None):
	r"""
	Returns a dictionary of the required context for the navbar.  If it is being used for a view that is inside a class pass the class id.
	
	If you are in a class view pass it the class_object, if you are in a category view pass it the category_object to generate the context correctly.
	
	Adds ``'top_level_categories'`` and ``'selected_categories'`` to the context.
	
	"""
	if category_object: # Find the selected categories
		context = get_parent_categories(category_object, class_object)
	else: # Still need to define context otherwise
		context = {}
	if class_object:
		context.update({
			'top_level_categories': class_object.category_set.filter(parent_categories=None)
		})
	else:
		context.update({
			'top_level_categories': BaseCategory.objects.filter(parent_categories=None)
		})
	return context
	
def has_class_access(class_object, user):
	r"""Returns True if the user is allowed to view the class page, False otherwise."""
	return (class_object.status == "N" and not (user.is_superuser or
			class_object.author == user or
		 	class_object.allowed_users.filter(id=user.id).exists()))
	
def get_context_for_atom(atom_object=None):
	r"""
	This function returns the context dictionary containing the context specific to an atom.
	
	It takes in the atom you want the context for.  If no input is given it returns a list of the required keys with empty lists as their values.
	
	"""
	if not atom_object:
		context = {'videos':[], 'expositions':[], 'notes':[], 'examples':[]}
	else:
		context = {
			'videos':atom_object.tags.distinct(),
			'expositions':atom_object.exposition_set.distinct(),
			'notes':atom_object.lecturenote_set.distinct(),
			'examples':atom_object.example_set.distinct()
		}
	return context
	
def get_context_for_category(category_object, context=None):
	"""
	This function returns context for category views.  It adds ``'videos'``, ``'expositions'``, ``'notes'``, ``'examples'``, and ``'atoms'`` to the context.  It requires the category you want to get the context for as an input.  ``category_object`` can be either a BaseCategory or an AtomCategory.
	
	"""
	if not context:
		first_call_flag = True # We only convert to list and get the distinct elements once
		context = get_context_for_atom() # Initialize context to dict of empty lists
		context.update({'atoms':[]}) # Add 'atoms' to the context which has atom specific keys in it
	else:
		first_call_flag = False # If its not the first loop we don't want to convert to distinct list
	temp = {'atoms':category_object.child_atoms.all()}
	for atom in temp['atoms']: # Only hits dict once to get into loop
		temp.update( # Get the context for 'atom'
			get_context_for_atom(atom)
		)
		for key in context: # Chain the keys together, chain is faster than using loops b/c it is in C
			context[key] = chain(context[key],temp[key])
	for child in category_object.child_categories.all(): # Get content for all child categories
		get_context_for_category(child, context) #recurse
	if first_call_flag: # Only do this on the top level of recursion
		for key in context:
			context[key] = list(set(context[key]))
	return context # Return the context

def get_parent_categories(current_category, current_class): # Look at for refactoring
	"""
	This function returns a context dictionary with ``'selected_categories'`` as all of the parent categories for ``current_category``.
	
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
	return {'selected_categories':parent_categories}