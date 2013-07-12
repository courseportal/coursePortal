r"""View helper functions."""
from itertools import chain

from web.models import Class, AtomCategory, BaseCategory, Atom, Submission, Example, Exposition, LectureNote

def get_navbar_context(class_object=None):
	r"""Returns a dictionary of the required context for the navbar.  If it is being used for a view that is inside a class pass the class id."""
	context = {}
	if class_object:
		context.update({
			'top_level_categories': class_object.category_set.filter(parent_category=None)
		})
	else:
		context.update({
			'top_level_categories': BaseCategory.objects.filter(parent_categories=None)
		})
	return context
	
	
def get_context_for_category(current_category, context=None):
	"""
	This function returns context for category views.  It adds ``'videos'``, ``'expositions'``, ``'notes'``, ``'examples'``, and ``'atoms'`` to the context.  It requires the category you want to get the context for as an input.  ``current_category`` can be either a BaseCategory or an AtomCategory.
	
	"""
	if not context:
		first_call_flag = True # We only convert to list and get the distinct elements once
		context = {'videos':[], 'expositions':[], 'notes':[], 'examples':[], 'atoms':[]} # Populate
	else:
		first_call_flag = False # If its not the first loop we don't want to convert to distinct list
	temp = {'atoms':current_category.child_atoms.all()}
	for atom in temp['atoms']: # Only hits dict once to get into loop
		temp.update({ # Get the content of this atom
			'videos':Submission.objects.filter(tags=atom).distinct(),
			'expositions':atom.exposition_set.all(),
			'notes':atom.lecturenote_set.all(),
			'examples':atom.example_set.all()
		})
		for key in context: # Chain the keys together, chain is faster than using loops b/c it is in C
			context[key] = chain(context[key],temp[key])
	for child in current_category.child_categories.all(): # Get content for all child categories
		get_context_for_category(child, context) #recurse
	if first_call_flag: # Only do this on the top level of recursion
		for key in context:
			context[key] = list(set(context[key]))
	return context # Return the context

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