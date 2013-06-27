from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from web.models import Class

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