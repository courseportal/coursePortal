import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
import string

def validate_umich_email(value):
    regex_umich_email = re.compile('\w*@umich.edu')
    if not regex_umich_email.match(value):
        raise ValidationError(u'%s is not a valid University of Michigan email address.' % value)

def validate_username(value):
    pattern = r'[^\_a-zA-Z0-9]'
    if re.search(pattern, value):
       raise ValidationError(u'%s is not valid username.' % value) 

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(
		widget=forms.PasswordInput,
		max_length=102,
		required=True
	)
    redirect = forms.CharField(
		widget=forms.widgets.HiddenInput,
		required=False
	)

class RegisterForm(forms.Form):
    firstname = forms.CharField(
		max_length=100,
		required=True,
		label=_('First Name')
	)
    lastname = forms.CharField(
		max_length=100,
		required=True,
		label=_('Last Name')
	)
    username = forms.CharField(
        max_length=100,
        required=True,
        label=_('Username'),
        validators=[validate_username],
        help_text=_('Only numbers, letters and _ are accepted .')
    )
    email = forms.EmailField(
		max_length=100,
		required=True,
		validators=[validate_umich_email],
		help_text=_('Only University of Michigan email addresses are currently allowed to be registered.')
	)
    password = forms.CharField(
		widget=forms.PasswordInput,
		max_length=100,
		required=True
	)
    password_confirmation = forms.CharField(
		widget=forms.PasswordInput,
		max_length=100,
		required=True,
		label=_('Confirm Password')
	)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
		widget=forms.PasswordInput,
		max_length=100,
		required=True
	)
    new_password = forms.CharField(
		widget=forms.PasswordInput,
		max_length=100,
		required=True
	)
    new_password_confirm = forms.CharField(
		widget=forms.PasswordInput,
		max_length=100,
		required=True,
		label=_('Confirm New Password')
	)
    action = forms.CharField(widget=forms.HiddenInput(), initial='password')

class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(
		max_length=100,
		required=True,
		label=_('Display Name')
	)
    action = forms.CharField(widget=forms.HiddenInput(), initial='username')

class DeleteAccountForm(forms.Form):
    confirmation = forms.CharField(
		max_length=100,
		required=True,
		label=_('Confirmation')
	)
    action = forms.CharField(
		widget=forms.HiddenInput(),
		initial='delete_account'
	)
