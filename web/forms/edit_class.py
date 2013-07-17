from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from web.models import Class, ClassCategory


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
		if self.instance: # Exclude self to prevent loops
			self.fields['parent_categories'].queryset = (
				ClassCategory.objects.filter(parent_class=
				self.parent_class).exclude(id=self.instance.id)
			)
		else:
			self.fields['parent_categories'].queryset = (
				ClassCategory.objects.filter(parent_class=self.parent_class)
			)
		
	
	class Meta:
		r"""Set the model it is attached to and select the fields."""
		model = ClassCategory
		fields=('title', 'parent_categories', 'child_atoms')
		
	def save(self, commit=True):
		r"""Overrides the save method."""
		instance = super(CategoryForm, self).save(commit=False)
		instance.parent_class = self.parent_class
		if commit:
			instance.save()
			self.save_m2m()

		return instance

class ClassForm(forms.ModelForm):
	r"""Form for **editing** classes."""
	def __init__(self, *args, **kwargs):
		"""Sets the queryset of ``instructors`` to exclude the author and save the user to ``self`` and make the ``instructors`` field not required."""
		self.user = kwargs.pop('user')
		super(ClassForm, self).__init__(*args, **kwargs)
		self.fields['instructors'].queryset = User.objects.exclude(
			id=self.user.id)
		self.fields['instructors'].required = False
	
	class Meta:
		r"""Set the model the form is attached to and select the fields."""
		model = Class
		fields = ('title', 'status', 'summary', 'instructors', 'students')
		
	#Clean categories so they can't have the same name?
		
class CreateClassForm(ClassForm):
	r"""Form for **creating** classes."""
	def save(self):
		r"""Overrides the save to add ``self.user`` to ``instructors`` and as an ``owner``."""
		instance = super(CreateClassForm, self).save(commit=False)
		instance.owner = self.user
		
		instance.save()
		self.save_m2m()
		instance.instructors.add(self.user)
			
		return instance
		