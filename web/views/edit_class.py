from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from web.forms.edit_class import CreateClassForm, CreateCategoryFormSet
from web.models import Class, AtomCategory

class CreateClassView(FormView):
	r"""View for the class creation form"""
	template_name = 'web/home/class_create_form.html'
	form_class = CreateClassForm
	success_url = reverse_lazy('class_index')
	
	def get_context_data(self, **kwargs):
		r"""Add the inline category formset to the view"""
		context = super(CreateClassView, self).get_context_data(**kwargs) # Returns a dictionary
		if self.request.POST:
			context['formset'] = CreateCategoryFormSet(self.request.POST)
			print('\n\n{}\n\n'.format(context['formset'].non_form_errors()))
		else:
			context['formset'] = CreateCategoryFormSet()
		return context
	
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(CreateClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
	
	def form_valid(self, form):
		r"""Gets called if the form is valid, in that case I save the form and change the 'success_url' to the newely created classes home page."""
		class_created = form.save_class(user=self.request.user)
		
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			formset.parent_class = class_created
			formset.save()
		else:
			return self.form_invalid(form)
		
		self.success_url = class_created.get_absolute_url()
		return super(CreateClassView, self).form_valid(form)		