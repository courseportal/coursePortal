r"""View helper functions."""
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