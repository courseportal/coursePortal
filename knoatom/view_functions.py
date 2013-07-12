import re

def get_breadcrumbs(path, name_function_dict={}):
	r"""
	Returns a dictionary of the required context for the breadcrumbs.
	
	It requires the path of the current view which is stored in ``request.path``.
	It also requires a dict of functions that return the name to be used with the breadcrumb.  The keys must correspond to the string arguments in the url.  The functions **must** accept a list of pks, even if they expect an empty list.  ``get_breadcrumbs`` will pass in a list of pks in the order they appear.  If there is no key cooresponding to the string argument ``get_breadcrumbs`` will use the string argument as the title.
	
	Example using a lambda and a normal function
	
	.. code::
	
		URL = '/list/item/1/'
		item_function(pks): # Expects len(pks) is 0
			pass
		arg_dict = {'list': lambda pks: 'List of Items', 'category': item_function}
		get_breadcrumbs(URL, arg_dict)
	
	"""
	
	dirty_argument_list = re.split('/', path) # Split the string up into a list of arguments
	dirty_argument_list = [elt for elt in dirty_argument_list if elt != ''] # Remove all '' from list
	argument_list = [] # The clean argument list
	for elt in dirty_argument_list: # Coerce all pk's to strings.
		try:
			argument_list.append(int(elt))
		except ValueError:
			argument_list.append(str(elt))
	breadcrumbs = []
	i = 1 # i will always be the element we are on + 1.
	for arg in argument_list:
		if type(arg) != str: # We don't want to do anything with ints in outer loop
			continue
		crumb = {'url': make_url(argument_list[:i])}
		pks = []
		name_function = name_function_dict.get(arg, arg)
		
		if type(name_function) == str: # There was no function cooresponding to 'arg' as a key
			crumb.update({
				'title': arg # So just make arg the title. 
			})
			breadcrumbs.append(crumb)
			continue # We don't need to do the rest of the loop
			
		for pk in argument_list[i:]: # Add following int arguments to pks until we hit a string
			if type(pk) != int: # Stop when we hit a string
				break
			pks.append(pk) # Add the argument to pks
		crumb.update({
			'title': name_function(pks) # Add the title to the crumb
		})
		breadcrumbs.append(crumb) # Append the crumb dict to the breadcrumbs list
		i += 1
	return {'breadcrumbs':breadcrumbs} # Return the dict containing the breadcrumbs.
			
			
def make_url(arg_list):
	r"""Takes in a list of arguments of a url split by '/' and returns the reformed url."""
	path = '/'
	for elt in arg_list:
		path += str(elt)+'/'
	return path