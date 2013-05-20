from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.forms.util import ErrorList
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
import hashlib
import logging
import random, string
from web.forms.account import *
from web.models import Category

@login_required()
def index(request):
    password_form = ChangePasswordForm(error_class=PlainErrorList)
    username_form = ChangeUsernameForm(error_class=PlainErrorList)
    delete_account_form = DeleteAccountForm(error_class=PlainErrorList)
    if request.method == 'POST':
        if request.POST.get('action') == 'password':
            password_form = ChangePasswordForm(request.POST, error_class=PlainErrorList)
            if password_form.is_valid() and password_form.cleaned_data['new_password'] == password_form.cleaned_data['new_password_confirm']:
                if not authenticate(username=request.user.username, password=password_form.cleaned_data['current_password']):
                    messages.warning(request, 'Please supply your current password')
                else:
                    user = User.objects.get(pk=request.user.id)
                    if user:
                        user.set_password(password_form.cleaned_data['new_password'])
                        user.save()
                        messages.success(request, 'Your password has been changed.')
                        return HttpResponseRedirect(reverse('account'))
            else:
                messages.warning(request, 'Could not change your password. Make sure you type the same password twice in the form below')
        elif request.POST.get('action') == 'username':
            username_form = ChangeUsernameForm(request.POST, error_class=PlainErrorList)
            if username_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                list_with_username = User.objects.filter(username=username_form.cleaned_data['new_username'])
                if len(list_with_username) > 0:
                    messages.warning(request, 'The display name %s is currently in use. Please choose a different display name.' % username_form.cleaned_data['new_username'])
                if user and len(list_with_username) == 0:
                    user.username = username_form.cleaned_data['new_username']
                    user.save()
                    messages.success(request, 'Your display name has been changed.')
                    return HttpResponseRedirect(reverse('account'))
            else:
                messages.warning(request, 'Could not change your display name.')

        elif request.POST.get('action') == 'delete_account':
            delete_account_form = DeleteAccountForm(request.POST, error_class=PlainErrorList)
            if delete_account_form.is_valid():
                user = User.objects.get(pk=request.user.id)
                if user and delete_account_form.cleaned_data['confirmation'] == 'KnoAtom':
                    user.delete()
                    auth_logout(request)
                    messages.success(request, 'Your account has been deleted. Thank for your time! --KnoAtom Staff')
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.warning(request, 'The confirmation was not correct, or we could not find your account. Sorry, try again.')
            else:
                messages.warning(request, 'We could not delete your account.')

    t = loader.get_template('account/index.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('account'), 'title': 'Account'}],
        'password_form': password_form,
        'username_form': username_form,
        'delete_account_form': delete_account_form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def forgot_password(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            user_check = User.objects.filter(email=form.cleaned_data['email'])
            if user_check.count() == 1:
                user = User.objects.get(email=form.cleaned_data['email'])
                if user:
                    logging.debug('Changing password for %s' % user)
                    new_password = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
                    send_mail('KnoAtom Password Reset', 'You requested to reset your password at knoatom.eecs.umich.edu. Here is your new password: ' + new_password + '\n\nIf you did not request this change, contact us immediatly.\n\n-- The Management', 'knoatom-webmaster@umich.edu', [user.email, 'knoatom-webmaster@umich.edu'])
                    user.set_password(new_password)
                    user.save()
                    logging.debug('Successfully changed password for %s: %s' % (user, new_password))
            messages.success(request, 'If we have your email on file, you should expect a password reset within a couple minutes to appear in your inbox.')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = ForgotPasswordForm(error_class=PlainErrorList)

    t = loader.get_template('account/forgot_password.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = LoginForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            logging.debug('Trying to log in %s: %s' % (form.cleaned_data['email'], form.cleaned_data['password']))
            users = User.objects.filter(email=form.cleaned_data['email'].strip())
            if users.count() == 1:
                u = users[0]
                user = authenticate(username=u.username, password=form.cleaned_data['password'])
                if user is not None:
                    logging.debug('Trying to log in user %s' % user)
                    if user.is_active == 0:
                        messages.warning(request, 'Please activate your account before you log in. Contact knoatom-webmaster@umich.edu if you need further assistance.')
                        return HttpResponseRedirect(reverse('login'))
                    auth_login(request, user)
                    if form.cleaned_data['redirect']: return HttpResponseRedirect(form.cleaned_data['redirect'])
                    return HttpResponseRedirect(reverse('home'))
		logging.debug('Could not find account %s' % form.cleaned_data['email'])
        messages.warning(request, 'Could not authenticate you. Try again.')
    else:
        form = LoginForm(initial={'redirect': request.GET.get('next', None),}, error_class=PlainErrorList)

    t = loader.get_template('account/login.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('login'), 'title': 'Login'}],
        'login_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        form = RegisterForm(request.POST, error_class=PlainErrorList)
        if form.is_valid():
            email_search = User.objects.filter(email=form.cleaned_data['email'])
            if len(email_search) > 0:
                messages.warning(request, 'Could not register you. Email is already registered.')
            if form.cleaned_data['password'] != form.cleaned_data['password_confirmation']:
                messages.warning(request, 'Passwords did not match. Please try again.')
            if len(email_search) == 0 and form.cleaned_data['password'] == form.cleaned_data['password_confirmation']:
                user = User.objects.create_user(form.cleaned_data['email'], form.cleaned_data['email'], form.cleaned_data['password']);
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.is_active = False
                user.save()
                m = hashlib.md5()
                m.update(user.email + str(user.date_joined).split('.')[0])
                send_mail('KnoAtom Registration', 'You have successfully registered at knoatom.eecs.umich.edu with the username ' + user.username + '. Please validate your account by going to ' + request.build_absolute_uri('validate') + '?email=' + user.email + '&validation=' + m.hexdigest() + ' . If you did not process this registration, please contact us as soon as possible.\n\n-- The Management', 'knoatom-webmaster@umich.edu', [user.email])
                messages.success(request, 'You have been registered. Please login to continue.')
                return HttpResponseRedirect(reverse('login'))
        messages.warning(request, 'Could not register you. Try again.')
    else:
        form = RegisterForm(error_class=PlainErrorList)

    t = loader.get_template('account/register.html')
    c = RequestContext(request, {
        'breadcrumbs': [{'url': reverse('home'), 'title': 'Home'}, {'url':reverse('register'), 'title': 'Register'}],
        'register_form': form,
        'parent_categories': Category.objects.filter(parent=None),
    })
    return HttpResponse(t.render(c))

def validate(request):
    if request.user.is_authenticated():
        messages.warning(request, 'You are already confirmed.')
        return HttpResponseRedirect(reverse('home'))
    if request.GET.get('validation', None) and request.GET.get('email', None):
        user = User.objects.get(email=request.GET.get('email'))
        m = hashlib.md5()
        m.update(user.email + str(user.date_joined))
        if m.hexdigest() == request.GET.get('validation'):
            user.is_active = True
            user.save()
            messages.success(request, 'Thank you for validating your email!')
            return HttpResponseRedirect(reverse('account'))
        else:
            messages.warning(request, 'There was an error processing your validation.')
            return HttpResponseRedirect(reverse('login'))

    messages.warning(request, 'Your reached a page in an invalid manner.')
    return HttpResponseRedirect(reverse('home'))
