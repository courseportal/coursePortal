from django.views.generic.edit import FormView
from web.forms.edit_class import CreateClassForm
from django.core.urlresolvers import reverse_lazy
from web.models import Class

class CreateClassView(FormView):
	template_name = 'web/home/class_create_form.html'
	form_class = CreateClassForm
	success_url = reverse_lazy('class_index')
	
		
	def get_form_kwargs(self):
		r"""Returns the **kwargs required to instantiate the form."""
		kwargs = super(CreateClassView, self).get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs
	
	def form_valid(self, form):
		class_created = form.save_class(user=self.request.user)
		self.success_url = class_created.get_absolute_url()
		return super(CreateClassView, self).form_valid(form)
		
		