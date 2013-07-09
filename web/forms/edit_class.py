from django import forms
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory, BaseModelFormSet
from django.utils.translation import ugettext_lazy as _
from web.models import Class, AtomCategory


class CategoryForm(forms.ModelForm):
	r"""
	Form for category editing or creation creation from within a class editing view.
	
	.. warning::
	
		This form assumes that you are only editing **one** category at a time.  Otherwise infinite loops can be formed.
	
	"""
	def __init__(self, *args, **kwargs):
		r"""Sets the queryset of categories to only allow categories in the current class"""
		self.parent_class = kwargs.pop('parent_class')
		super(CategoryForm, self).__init__(*args, **kwargs)
		if self.instance: # Exclude model instance from the queryset to prevent loops
			self.fields['child_categories'].queryset = AtomCategory.objects.filter(parent_class=self.parent_class).exclude(id=self.instance.id)
		else:
			self.fields['child_categories'].queryset = AtomCategory.objects.filter(parent_class=self.parent_class)
		
	
	class Meta:
		r"""Set the model it is attached to and select the fields."""
		model = AtomCategory
		fields=('category_name', 'child_categories', 'child_atoms')
		
	def save(self):
		r"""Overrides the save method."""
		instance = super(CategoryForm, self).save(commit=False)
		instance.parent_class = self.parent_class
		instance.save()
		instance.child_categories = self.cleaned_data['child_categories']
		instance.child_atoms = self.cleaned_data['child_atoms']
		return instance

class ClassForm(forms.ModelForm):
	r"""Form for **editing** classes."""
	def __init__(self, *args, **kwargs):
		"""Sets the queryset of ``allowed_users`` to exclude the author and save the user to ``self`` and make the ``allowed_users`` field not required."""
		self.user = kwargs.pop('user')
		super(ClassForm, self).__init__(*args, **kwargs)
		self.fields['allowed_users'].queryset = User.objects.exclude(id=self.user.id)
		self.fields['allowed_users'].required = False
	
	class Meta:
		r"""Set the model the form is attached to and select the fields."""
		model = Class
		fields = ('name', 'status', 'summary', 'allowed_users', 'students')
		
	#Clean categories so they can't have the same name?
		
class CreateClassForm(ClassForm):
	r"""Form for **creating** classes."""
	def save(self):
		r"""Overrides the save to add ``self.user`` to ``allowed_users`` and as an ``author``."""
		instance = super(CreateClassForm, self).save(commit=False)
		instance.author = self.user
		instance.save()
		instance.allowed_users = self.cleaned_data['allowed_users']
		instance.allowed_users.add(self.user)
		instance.students = self.cleaned_data['students']
		return instance
		