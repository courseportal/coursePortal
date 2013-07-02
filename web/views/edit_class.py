import json

from django.http import HttpResponse
from django.views.generic.edit import FormView, CreateView
from django.core.urlresolvers import reverse_lazy
from web.forms.edit_class import CreateClassForm, CreateCategoryFormSet
from web.models import Class, AtomCategory

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
			print('\n\ninvalid\n\n')
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
			print('\n\nValid\n\n')
			data = {
				'pk': self.object.pk,
			}
			return self.render_to_json_response(data)
		else:
			return response
		
class CreateClassView(AjaxableResponseMixin, CreateView):
	form_class = CreateClassForm
	model = Class
		
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(CreateClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
		
def EditClassView(resonse, class_id):
	form_class = CreateClassForm
	template_name = "web/class_form.html"
	success_url = reverse_lazy('edit-class')
	
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(EditClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
		
	def form_invalid(self, form):
		pass
	def form_valid(self, form):
		pass
		
class OldCreateClassView(FormView):
	r"""View for the class creation form"""
	template_name = 'web/home/class_create_form.html'
	form_class = CreateClassForm
	success_url = reverse_lazy('class_index')
	
	def get_context_data(self, **kwargs):
		r"""Add the inline category formset to the view"""
		context = super(OldCreateClassView, self).get_context_data(**kwargs) # Returns a dictionary
		if self.request.POST:
			context['formset'] = CreateCategoryFormSet(self.request.POST)
			print('\n\n{}\n\n'.format(context['formset'].non_form_errors()))
		else:
			context['formset'] = CreateCategoryFormSet()
		return context
	
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(OldCreateClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
	
	def form_valid(self, form):
		r"""Gets called if the form is valid, in that case I save the form and change the 'success_url' to the newely created classes home page."""
		self.object = form.save_class(user=self.request.user)
		
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			formset.parent_class = self.object
			formset.save()
		else:
			return self.form_invalid(form)
		
		self.success_url = class_created.get_absolute_url()
		return super(OldCreateClassView, self).form_valid(form)		