import json

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse_lazy, reverse
from web.forms.edit_class import CreateClassForm, CategoryForm, ClassForm
from django.template import RequestContext, loader
from web.models import Class, AtomCategory, BaseCategory
from django.contrib import messages
from django.shortcuts import get_object_or_404, render

class AjaxableResponseMixin(object):
	r"""
	Mixin to add AJAX support to a form.
	Must be used with an object-based FormView.
	"""
	def render_to_json_response(self, context, **response_kwargs):
		data = json.dumps(context)
		response_kwargs['content_type'] = 'application/json'
		return HttpResponse(data, **response_kwargs)
		
	def form_invalid(self, form):
		response = super(AjaxableResponseMixin, self).form_invalid(form)
		if self.request.is_ajax():
			return self.render_to_json_response(form.errors)
		else:
			return response
		
	def form_valid(self, form):
		r"""
		We make sure to call the parent's form_valid() method because
		it might do some processing (in the case of CreateView, it will
		call form.save() for example).
		"""
		response = super(AjaxableResponseMixin, self).form_valid(form)
		if self.request.is_ajax():
			data = {
				'pk': self.object.pk,
			}
			return self.render_to_json_response(data)
		else:
			return response
		
class CreateClassView(AjaxableResponseMixin, CreateView):
	r"""View for creating class.  Handles both normal and AJAX requests."""
	form_class = CreateClassForm
	model = Class
	#template='web/class_form.html'
	
	def get_success_url(self):
		r"""Overrides the default function to return the correct url."""
		return reverse('edit_class', args=[self.object.id])
		
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(CreateClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
		
def EditClassView(request, class_id, cat_id):
	r"""View for editing classes."""
	context = {} # The context data
	class_object = get_object_or_404(Class, id=class_id) # The class instance
	class_form_kwargs = {'user':request.user, 'instance':class_object}
	category_form_kwargs = {'parent_class':class_object}
	if cat_id: # If we are editing a category
		category_object = get_object_or_404(AtomCategory, pk=cat_id)
		category_form_kwargs.update({'instance':category_object})
	if request.method == 'POST':
		if request.POST['form-type'] == 'submit-class': # If user pressed the Class submit button
			class_form = ClassForm(request.POST, **class_form_kwargs) # Bind class the form
			dicti = process_forms(request, class_object, class_form=class_form)
			context.update(dicti)
		elif request.POST['form-type'] == 'submit-category': # If user pressed Category submit button
			category_form = CategoryForm(request.POST, **category_form_kwargs) # Bind category form
			context.update(process_forms(request, class_object, category_form=category_form))
		else: # If the user pressed the submit everything button
			class_form = ClassForm(request.POST, **class_form_kwargs) # Bind the class form
			category_form = CategoryForm(request.POST, **category_form_kwargs) # Bind category form
			context.update(process_forms(request, class_object, class_form, category_form))
		if request.is_ajax(): # We don't need to return all of the context, just the update stuff
			return render_to_json_response(context)
		elif cat_id: # We don't want to allow users to access the page with cat_id, only AJAX	
			return HttpResponseRedirect(reverse('edit_class', args=[class_id]))
	else: # GET
		if request.is_ajax(): # Return a category form with initial data or with no data
			category_form = CategoryForm(**category_form_kwargs)
			template = loader.get_template('web/category_form_template.html')
			c = RequestContext(request, {'form':category_form})
			form_html = template.render(c) # HTML for the form
			context.update({
			'category_form':form_html
			})
			return render_to_json_response(context) # Return the html for the new form
		elif cat_id: # We don't allow GET requests with a category already set that aren't AJAX
			return HttpResponseRedirect(reverse('edit_class', args=[class_id]))
			
		context.update({ # We need to add the forms to the kwargs if its not POST
			'class_form':ClassForm(**class_form_kwargs),
			'category_form':CategoryForm(**category_form_kwargs)
		})
	# AJAX requests should not reach here because they should all be POST.
	# Pick the category header
	context.update({
		'pk':class_object.id,
		'top_level_categories':BaseCategory.objects.filter(parent_categories=None),
		'breadcrumbs':[{'url':reverse('edit_class', args=[class_id]), 'title':'Edit Class'}]
	})
	return render(request, 'web/class_edit_form.html', context)
	
	

# Helper functions for EditClassView
def process_forms(request, class_object, class_form=None, category_form=None):
	r"""
	Handles the form processing for 'EditClassView'.  It returns a dictionary of the context.  It supports both forms submitted normally and through AJAX.
	
	..note::
	
		This method **does NOT** add the form itself to the context because it is simpler to add that at the end of the view.
	
	"""
	class_form_kwargs = {'user':request.user, 'instance':class_object}
	category_form_kwargs = {'parent_class':class_object}
	
	context = {}
	if class_form: # If we were passed an instane of class_form
		if class_form.is_valid():
			class_form.save()
			context.update({'pk':class_object.id})
			if request.is_ajax():
				context.update({
					'message':'Successfully saved class.'
				})
			else:
				context.update({'class_form':class_form}) # Return the same form to the context
				messages.success(request, 'Successfully saved class.')
		else: #form not valid
			if request.is_ajax():
				context.update(class_form.errors)
				context.update({'message':'Error saving class.'})
			else:
				context.update({'class_form':class_form})
				messages.error(request, 'Error saving class.')
	if category_form: # If we were passed an instance of category_form
		if category_form.is_valid():
			category_form.save()
			context.update({'pk':class_object.id})
			if request.is_ajax():
				template = loader.get_template('web/category_form_template.html')
				c = RequestContext(request, {'form':CategoryForm(**category_form_kwargs)})
				form_html = template.render(c)
				context.update({
					'category_form': form_html,
					'message':'Successfully saved category.'
				})
			else:
				context.update({'category_form':CategoryForm(**category_form_kwargs)}) # Need new form
				messages.success(request, 'Successfully saved category.')
		else: # form is not valid
			if request.is_ajax():
				context.update(category_form.errors)
				context.update({'message':'Error saving category.'})
			else:
				context.update({'category_form':category_form})
				messages.error(request, 'Error saving category.')
	return context
	
# View to delete categories
def delete_category(request, pk):
	r"""
	Deletes the category with pk=pk and returns html for an empty category form.
	
	.. warning::
	
		This view is designed to only be used with AJAX
	
	"""
	if not request.is_ajax(): # If it is not an AJAX request return a 400 status code
		return HttpResponseBadRequest()
	category_object = get_object_or_404(AtomCategory, pk=pk)
	class_object = category_object.parent_class
	category_object.delete()
	category_form = CategoryForm(parent_class=class_object)
	
	template = loader.get_template('web/category_form_template.html')
	c = RequestContext(request, {'form':category_form})
	form_html = template.render(c)
	context = {
		'category_form': form_html,
		'message': 'Successfully deleted category.'
	}
	data = json.dumps(context)
	return HttpResponse(data, content_type='application/json')

# View to get children for columnview
def get_children(request, is_class, pk):
	r"""
	Returns an html list of the child atoms and categories of either the class or category in the correct format for columnview.
	
	.. warning::
	
		This view is designed to only be used with AJAX
	
	"""
	if not request.is_ajax():
		return HttpResponseBadRequest()
	is_class = int(is_class)
	if is_class:
		cur_class = get_object_or_404(Class, pk=pk)
		categories = cur_class.category_set.filter(parent_categories=None)
		atoms = []
	else:
		obj = get_object_or_404(AtomCategory, pk=pk)
		atoms = obj.child_atoms.all()
		categories = obj.child_categories.all()
	
	context = RequestContext(request, {'atoms':atoms, 'categories':categories})
	template = loader.get_template('web/category_list.html')
	data = json.dumps(template.render(context))
	return HttpResponse(data,content_type='application/json')
	
def get_category_form(request, pk):
	r"""Returns the html for a new populated category form."""
	obj = get_object_or_404(AtomCategory, pk=pk)
	

def render_to_json_response(context, **response_kwargs):
	data = json.dumps(context)
	response_kwargs['content_type'] = 'application/json'
	return HttpResponse(data, **response_kwargs)