from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _
from web.models import Class, AtomCategory

class BaseCreateCategoryFormSet(BaseModelFormSet):
	r"""Provide custom functionality to the category formset.  Functions are ordered in approximately the order that they are called"""	
	
	def __init__(self, *args, **kwargs):
		r"""Currently uses a quick fix because the django code is buggy (see _<Bug Report(https://code.djangoproject.com/ticket/17478)>).  When the bug is fixed change to regular version."""
		self.parent_class = kwargs.pop('parent_class', None)
		if self.parent_class:
			#self.queryset = 
			kwargs['queryset'] = AtomCategory.objects.filter(parent_class=self.parent_class)
		else:
			#self.queryset = 
			kwargs['queryset'] = AtomCategory.objects.none()
		super(BaseCreateCategoryFormSet, self).__init__(*args, **kwargs)
			
	def _construct_forms(self):
		self.forms = []
		for i in xrange(self.total_form_count()):
			self.forms.append(self._construct_form(i, parent_class=self.parent_class))
			
	def clean(self):
		r"""Disallows categories to have the same name."""
		super(BaseCreateCategoryFormSet, self).clean()
		names = []
		for form in self.forms:
			name = form.cleaned_data.get('name', None)
			if name in names:
				raise forms.ValidationError(_("Category name must be unique in this class."), code="duplicate")
			names.append(name)
			
	def save(self):
		r"""Saves the categories defined in the formset."""
		categories = super(BaseCreateCategoryFormSet, self).save(commit=False)
		for category in categories:
			category.parent_class = self.parent_class
			category.save()
		return categories
		
class CategoryForm(forms.ModelForm):
	r"""Form for category creation"""
	def __init__(self, *args, **kwargs):
		r"""Sets the queryset of categories to only allow categories in the current class"""
		cur_class = kwargs.pop('parent_class', None)
		super(CategoryForm, self).__init__(*args, **kwargs)
		if cur_class:
			self.fields['child_categories'].queryset = AtomCategory.objects.filter(parent_class=cur_class)
		else:
			self.fields['child_categories'].queryset = AtomCategory.objects.none()
	
	class Meta:
		model = AtomCategory
			
			
CreateCategoryFormSet = modelformset_factory(
	AtomCategory, 
	formset=BaseCreateCategoryFormSet,
	form=CategoryForm,
	fields=('name', 'child_categories', 'child_atoms'),
	extra=1,
)

class CreateClassForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		"""Sets the queryset of 'allowed_users' to exclude the author"""
		user = kwargs.pop('user')
		super(CreateClassForm, self).__init__(*args, **kwargs)
		self.fields['allowed_users'].queryset = User.objects.exclude(id=user.id)
		
	allowed_users = forms.ModelMultipleChoiceField(label='Instructors', required=False, queryset=User.objects.none())
	
	class Meta:
		model = Class
		fields = ('name', 'summary', 'status', 'allowed_users', 'students')
		
	def save_class(self, user):
		r"""Saves the model using the self.cleaned_data dictionary and user as the 'author'.  Adds 'author' to 'allowed_users'.  Returns the class that was created."""
		new_class = Class.objects.create(
			name=self.cleaned_data['name'],
			summary=self.cleaned_data['summary'],
			status=self.cleaned_data['status'],
			author=user,
		)
		new_class.allowed_users = self.cleaned_data['allowed_users']
		new_class.allowed_users.add(user)
		new_class.students = self.cleaned_data['students']
		return new_class
		
class EditClassForm(CreateClassForm):
	r"""Same as CreateClassForm except for the save_class method."""
	def save_class(self, user):
		r"""Overrides CreateClassForm's 'save_class' method"""