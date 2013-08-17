from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import random, string, re
from web.forms.admin import *
from knoatom.view_functions import get_breadcrumbs
from web.views.view_functions import web_breadcrumb_dict

@login_required()
def batch_add(request):
	if not request.user.is_staff:
		return HttpResponseRedirect(reverse('home'))

	if request.method == 'POST':
		form = BatchAddUsersForm(request.POST)
		if form.is_valid():
			users_added = 0
			for u in form.cleaned_data['users'].split('\n'):
				u = u.strip()
				if u == '': continue
				user_exists = User.objects.filter(
					Q(email=u)|Q(username=u)).exists()
				if not re.match('[a-z]*@umich\.edu', u) or user_exists:
					messages.warning(request, 'Could not add ' + u + 
						'. Username or email are already in the database, or '
						'email is not uniqname@umich.edu.'
					)
					continue
				password = ''.join(random.choice(string.ascii_uppercase + 
					string.digits + string.ascii_lowercase) for x in range(10))
				user = User.objects.create_user(email=u, username=u)
				user.set_password(password)
				user.save()
				users_added += 1
				send_mail(
					subject='KnoAtom New Account',
					message='You have been registered at '
						'knoatom.eecs.umich.edu. Your information is as '
						'follows:\n\nUsername: ' + u + '\nPassword: ' +
						 password + '\n\nPlease login and change your '
						 'password as soon as you can (click on your username '
						 'at the bottom of the left sidebar).\n\nThank '
						 'you\n\n-- The Management',
					recipient_list=[u, 'knoatom-webmaster@gmail.com']
				)
			messages.success(request, str(users_added) + ' users have been '
				'added.')
		else:
			messages.warning(request, 'Could not add users. Did you have the '
				'format correct?')
	else:
		form = BatchAddUsersForm()
	context = get_breadcrumbs(request.path, web_breadcrumb_dict)
	context.update({'form':form})
	return request(render, 'web/admin/batch_add.html', context)

# @login_required()
# def list_videos(request):
#     if not request.user.is_staff:
#         return HttpResponseRedirect(reverse('home'))
# 
#     top_ranked_videos = cache.get('top_ranked_videos') # Load from cache
#     if top_ranked_videos is None: # If there is no cached version
#         top_ranked_videos = Video.objects.all().order_by('-votes')[:5]
#         cache.set('top_ranked_videos', top_ranked_videos, 60*10) # Set cache
#     
#     context = get_breadcrumbs(request.path, web_breadcrumb_dict)
#     context.update({'top_ranked_videos':top_ranked_videos})
#     return render(request, 'web/admin/videos.html', context)
