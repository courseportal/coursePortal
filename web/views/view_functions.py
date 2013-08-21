r"""View helper functions."""
from itertools import chain
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from web.models import Class, ClassCategory, BaseCategory, Atom, Content

# Dict to pass to the breadcrumb function to work with all of web.
web_breadcrumb_dict = {
    'class-index':  lambda pks: 'Class List',
    'class':        lambda pks: get_object_or_404(Class, pk=pks[0]),
    'category':     lambda pks: get_object_or_404(ClassCategory, pk=pks[0]),
    'base-category':lambda pks: get_object_or_404(BaseCategory, pk=pks[0]),
    'atom':         lambda pks: get_object_or_404(Atom, pk=pks[0]),
    'submit-content':   lambda pks: get_submit_url(pks, Content),
    'create-class': lambda pks: 'Create Class',
    'edit-class':   lambda pks: 'Edit ' + str(get_object_or_404(Class,                                     pk=pks[0])),
    'account':      lambda pks: 'Account Management',
    'forgot-password':  lambda pks: 'Forgot Password',
    'login':        lambda pks: 'Login',
    'register':     lambda pks: 'Register',
    'batch-add':    lambda pks: 'Add Multiple Users',
    'content':      lambda pks: (str(get_object_or_404(Content, pk=pks[0])) + 
                                 ' Details')
    #'view-videos':    lambda pks: 'View All Videos',
}

def get_submit_url(pks, ObjectClass):
    r"""Returns the name of submission form pages.  ``ObjectClass`` is the class of the object.  If pks is an empty list it uses ``ObjectClass.__name__`` as the name."""
    if pks != []:
        return 'Edit ' + str(get_object_or_404(ObjectClass, pk=pks[0]))
    else:
        return 'Submit ' + ObjectClass.__name__

def get_navbar_context(category_object=None, class_object=None):
    r"""
    Returns a dictionary of the required context for the navbar.  If it is being used for a view that is inside a class pass the class id.
    
    If you are in a class view pass it the class_object, if you are in a category view pass it the category_object to generate the context correctly.
    
    Adds ``'top_level_categories'`` and ``'selected_categories'`` to the context.
    
    ``if class_object is not None`` then it will fetch the ``ClassCategory`` set that is in the class otherwise it will fetch the ``BaseCategory`` set as ``'top_level_categories'``.  ``'selected_categories'`` are the categories that should be highlighted
    
    """
    if category_object is not None: # Find the selected categories
        context = get_parent_categories(category_object, class_object)
    else: # Still need to define context otherwise
        context = {}
    if class_object is not None:
        context.update({
            'top_level_categories': ( 
                class_object.category_set.filter(parent_categories=None)
            )
        })
    else:
        context.update({
            'top_level_categories': (
                BaseCategory.objects.filter(parent_categories=None)
            )
        })
    return context
    
def has_class_access(class_object, user):
    r"""Returns True if the user is allowed to view the class page, False otherwise."""
    return (class_object.status == "N" and not (user.is_superuser or
            class_object.owner == user or
             class_object.instructors.filter(id=user.id).exists()))
    
def get_context_for_atom(atom_object=None):
    r"""
    This function returns the context dictionary containing the context specific to an atom.
    
    It takes in the atom you want the context for.  If no input is given it returns a list of the required keys with empty lists as their values.
    
    """
    if atom_object is None:
        context = {'content_list':[(),(),(),()]}
    else:
        content = atom_object.content_set.all()
        content_list = []
        content_types = Content.CONTENT_TYPES
        types = {}
        for i in range(0, len(content_types)):
            content_list.append([])
            types[content_types[i][0]] = i
        for c in content:
            content_list[types[c.content_type]].append(c)
        for i in range(0, len(content_list)):
            content_list[i] = tuple(content_list[i])
        context = {
            'atom_object':atom_object,
            'content_list':content_list
        }
    return context
    
def get_context_for_category(category_object, context=None):
    """
    This function returns context for category views.  It adds ``'videos'``, ``'expositions'``, ``'notes'``, ``'examples'``, and ``'atoms'`` to the context.  It requires the category you want to get the context for as an input.  ``category_object`` can be either a BaseCategory or an ClassCategory.
    
    """
    if context is None:
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
        context_list_new = []
        content_list_final = []
        atoms_list_new = []
        for i in range(0,4):
            context_tuple=tuple(context["content_list"])[i] + tuple(temp["content_list"])[i]
            context_list_new.append(context_tuple)
        context["atoms"] = chain(context["atoms"],temp["atoms"])
        for i in context["atoms"]:
            atoms_list_new.append(i)

        context["content_list"] = context_list_new
        context["atoms"] = atoms_list_new
        for i in range(0,4):
            content_list_set = set(tuple(context["content_list"])[i])
            content_list_final.append(tuple(content_list_set))
        context["content_list"] = content_list_final


        #for key in context:  # Chain the keys together, chain is faster than using loops b/c it is in C
        #    context[key] = chain(context[key],temp[key])

    for child in category_object.child_categories.all(): # Get content for all child categories
        get_context_for_category(child, context) #recurse
    #if first_call_flag: # Only do this on the top level of recursion
    #    for key in context:
    #        seq = context[key]
    #        seen = set()
    #        seen_add = seen.add
    #        context[key]=[ x for x in seq if x not in seen and not seen_add(x)]
            #context[key] = list(set(context[key])) # Remove duplicates
    return context # Return the context

def get_parent_categories(category_object, class_object): # Look at for refactoring
    """
    This function returns a context dictionary with ``'selected_categories'`` as all of the parent categories for ``category_object``.
    
    If ``class_object`` is ``None`` then it will filter the parent_categories list to only include categories that are in ``class_object``, otherwise it will return all parent categories.
    
    .. warning::
        
        If there are loops in your categories this will result in infinite loops, but you shouldn't be able to create categories in the admin site that result in infinite loops.
    
    """
    parent_categories=list()
    parent_categories.append(category_object)
    if class_object is not None:
        tmp_categories = category_object.parent_categories.filter(parent_class=class_object)
    else:
        tmp_categories = category_object.parent_categories.all()
    while tmp_categories:
        parent_categories.append(tmp_categories[0])
        if class_object is not None:
            tmp_categories = tmp_categories[0].parent_categories.filter(parent_class=class_object)
        else:
            tmp_categories = tmp_categories[0].parent_categories.all()
    return {'highlighted_categories':parent_categories}