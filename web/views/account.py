from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.template import loader, RequestContext
from django.shortcuts import render
from django.conf import settings
import hashlib
import logging
import random, string
from web.forms.account import *
from rating.models import UserRating
from knoatom.view_functions import get_breadcrumbs
from web.views.view_functions import web_breadcrumb_dict

@login_required()
def index(request):
    user_rate = UserRating.objects.get(user=request.user)
    if request.method == 'POST':
        if request.POST.get('action') == 'password': # Password form processing
            password_form = ChangePasswordForm(request.POST)
            if (password_form.is_valid() and
                    password_form.cleaned_data['new_password'] == 
                    password_form.cleaned_data['new_password_confirm']):
                if not authenticate(username=request.user.username, 
                        password=password_form.cleaned_data['current_password']
                        ):
                    messages.warning(
                        request,
                        _('Please supply your current password')
                    )
                else:
                    user = User.objects.get(pk=request.user.id)
                    if user:
                        user.set_password(
                            password_form.cleaned_data['new_password']
                        )
                        user.save()
                        messages.success(
                            request,
                            'Your password has been changed.'
                        )
                        return HttpResponseRedirect(reverse('account'))
            else:
                messages.warning(
                    request,
                    _('Could not change your password. Make sure you type the '
                    'same password twice in the form below')
                )
        elif request.POST.get('action') == 'username':#Username form processing
            username_form = ChangeUsernameForm(request.POST)
            if username_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                list_with_username = User.objects.filter(
                    username=username_form.cleaned_data['new_username']
                ).exists
                if User.objects.filter(
                            username=username_form.cleaned_data['new_username']
                        ).exists():
                    messages.warning(
                        request,
                        _('The display name %s is currently in use. Please '
                            'choose a different display name.' %
                            username_form.cleaned_data['new_username']
                        )
                    )
                elif user:
                    user.username = username_form.cleaned_data['new_username']
                    user.save()
                    messages.success(
                        request,
                        _('Your display name has been changed.')
                    )
                    return HttpResponseRedirect(reverse('account'))
            else:
                messages.warning(
                    request,
                    _('Could not change your display name.')
                )

        elif request.POST.get('action') == 'delete_account':#delete form
            delete_account_form = DeleteAccountForm(request.POST)
            if delete_account_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                if (user and delete_account_form.cleaned_data['confirmation'] 
                        == 'KnoAtom'):
                    user.delete()
                    auth_logout(request)
                    messages.success(request, _('Your account has been '
                        'deleted. Thank for your time! --KnoAtom Staff')
                    )
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.warning(request, _('The confirmation was not '
                        'correct, or we could not find your account. Sorry, '
                        'try again.')
                    )
            else:
                messages.warning(request, _('We could not delete your '
                    'account.')
                )
    else: # Request is not POST
        password_form = ChangePasswordForm()
        username_form = ChangeUsernameForm()
        delete_account_form = DeleteAccountForm()
        
    context = get_breadcrumbs(request.path, web_breadcrumb_dict)
    context.update({
        'password_form': password_form,
        'username_form': username_form,
        'delete_account_form': delete_account_form,
        'user_rate': user_rate,
    })
    return render(request, 'web/account/index.html', context)

def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            user_check = User.objects.filter(email=form.cleaned_data['email'])
            if user_check.count() == 1:
                user = User.objects.get(email=form.cleaned_data['email'])
                if user:
                    logging.debug('Changing password for %s' % user)
                    new_password = ''.join(random.choice(
                            string.ascii_uppercase + string.digits + 
                            string.ascii_lowercase
                        ) for x in range(10))
                    send_mail(
                        subject=_('KnoAtom Password Reset'),
                        message=_('You requested to reset your password at '
                            'knoatom.eecs.umich.edu. Here is your new '
                            'password: ') + new_password + _('\n\nIf you did '
                            'not request this change, contact us '
                            'immediatly.\n\n--The Management'),
                        from_email='knoatom-noreply@gmail.com',
                        recipient_list=[user.email, EMAIL_HOST_USER]
                    )
                    user.set_password(new_password)
                    user.save()
                    logging.debug('Successfully changed password for %s: %s' %
                        (user, new_password)
                    )
            messages.success(request, _('If we have your email on file, you '
                'should expect a password reset within a couple minutes to '
                'appear in your inbox.')
            )
            return HttpResponseRedirect(reverse('login'))
    else:
        form = ForgotPasswordForm()
    context = get_breadcrumbs(request.path, web_breadcrumb_dict)
    context.update({
        'login_form': form
    })
    return render(request, 'web/account/forgot_password.html', context)

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            logging.debug('Trying to log in %s: %s' %
                (form.cleaned_data['email'], form.cleaned_data['password'])
            )
            users = User.objects.filter(
                email=form.cleaned_data['email'].strip()
            )
            if users.count() == 1:
                u = users[0]
                user = authenticate(
                    username=u.username, 
                    password=form.cleaned_data['password']
                )
                if user is not None:
                    logging.debug('Trying to log in user %s' % user)
                    if user.is_active == 0:
                        messages.warning(request, _('Please activate your '
                            'account before you log in. Contact '
                            'knoatom-webmaster@umich.edu if you need further '
                            'assistance.')
                        )
                        return HttpResponseRedirect(reverse('login'))
                    else:
                        auth_login(request, user)
                    if form.cleaned_data['redirect']:
                        return HttpResponseRedirect(
                            form.cleaned_data['redirect']
                        )
                    else:
                        return HttpResponseRedirect(reverse('home'))
        logging.debug('Could not find account %s' % form.cleaned_data['email'])
        messages.warning(request, _('Could not authenticate you. Try again.'))
    else: # Request is GET
        form = LoginForm(initial={'redirect':request.GET.get('next', None)})
        
    context = get_breadcrumbs(request.path, web_breadcrumb_dict)
    context.update({'login_form':form})
    return render(request, 'web/account/login.html', context)
    
@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email_exists = User.objects.filter(
                email=form.cleaned_data['email']
            ).exists()
            if email_exists:
                messages.warning(request, _('Could not register you. Email is '
					'already registered.')
				)
            if (form.cleaned_data['password'] !=
					form.cleaned_data['password_confirmation']):
				messages.warning(request, _('Passwords did not match. Please '
					'try again.')
				)
            elif not email_exists:
                user = User.objects.create_user(
                    form.cleaned_data['email'], form.cleaned_data['email'],
                    form.cleaned_data['password']
				)
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.username = form.cleaned_data['username']
                user.is_active = False
                user.save()
                m = hashlib.md5()
                m.update(user.email + str(user.date_joined).split('.')[0])
                send_mail(
					subject=_('KnoAtom Registration'), 
					message=(_('You have successfully registered at '
						'knoatom.eecs.umich.edu with the username ') + 
						user.username +
						 _('. Please validate your account by going to ')+ 
					 	request.build_absolute_uri('validate')+'?email='+ 
					 	user.email + '&validation=' + m.hexdigest() + 
					 	_(' . If you did not process this registration, '
						'please contact us as soon as possible.\n\n-- The '
						'Management')
					),
					from_email='knoatom-noreply@gmail.com', 
					recipient_list=[user.email, EMAIL_HOST_USER], 
					fail_silently=False
				)
                messages.success(request, _('You have been registered. Please '
					'login to continue.')
				)
                return HttpResponseRedirect(reverse('login'))
		
        messages.warning(request, _('Could not register you. Try again.'))
    else: # Request is GET
        form = RegisterForm()
	
=======
                )
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.is_active = False
                user.save()
                m = hashlib.md5()
                m.update(str(user.email) + 
                    str(user.date_joined).split('.')[0].split('+')[0])
                send_mail(
                    subject=_('KnoAtom Registration'), 
                    message=(_('You have successfully registered at '
                        'knoatom.eecs.umich.edu with the username ') + 
                        user.username +
                         _('. Please validate your account by going to ')+ 
                         request.build_absolute_uri('validate')+'?email='+ 
                         user.email + '&validation=' + m.hexdigest() + 
                         _(' . If you did not process this registration, '
                        'please contact us as soon as possible.\n\n-- The '
                        'Management')
                    ),
                    from_email='knoatom-noreply@gmail.com', 
                    recipient_list=[user.email, settings.EMAIL_HOST_USER], 
                    fail_silently=False
                )
                messages.success(request, _('You have been registered. Please '
                    'login to continue.')
                )
                return HttpResponseRedirect(reverse('login'))
        
        messages.warning(request, _('Could not register you. Try again.'))
    else: # Request is GET
        form = RegisterForm()
    
>>>>>>> ebbeb6e34c81f3ca15ee6defa341b11a07f8e1db
    context = get_breadcrumbs(request.path, web_breadcrumb_dict)
    context.update({'register_form':form})
    return render(request, 'web/account/register.html', context)

def validate(request):
    if request.user.is_authenticated():
        messages.warning(request, _('You are already confirmed.'))
        return HttpResponseRedirect(reverse('home'))
    if request.GET.get('validation', None) and request.GET.get('email', None):
        user = User.objects.get(email=request.GET.get('email'))
        m = hashlib.md5()
        m.update(str(user.email) + 
            str(user.date_joined).split('.')[0].split('+')[0])
        if m.hexdigest() == request.GET.get('validation'):
            user.is_active = True
            user.save()
            messages.success(request,_('Thank you for validating your email!'))
            return HttpResponseRedirect(reverse('account'))
        else:
            messages.warning(request, _('There was an error processing your '
                'validation.')
            )
            return HttpResponseRedirect(reverse('login'))

    messages.warning(request, _('Your reached a page in an invalid manner.'))
    return HttpResponseRedirect(reverse('home'))
