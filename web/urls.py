from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/(?P<bid>\d+)?/?$', 'web.views.account.login', name='login'),
    url(r'^logout/', 'web.views.account.logout', name='logout'),
    url(r'^register/(?P<bid>\d+)?/?$', 'web.views.account.register', name='register'),
    url(r'^validate/$', 'web.views.account.validate', name='validate'),
    url(r'^forgot_password/(?P<bid>\d+)?/?$', 'web.views.account.forgot_password', name='forgot_password'),
    url(r'^account/(?P<bid>\d+)?/?$', 'web.views.account.index', name='account'),

    url(r'^batch_add/?$', 'web.views.admin.batch_add', name='batch_add'),
    url(r'^view_videos/?$', 'web.views.admin.list_videos', name='list_videos'),

    url(r'^ajax/vote/(\d+)/(\d+)/(\d+)/?$', 'web.views.ajax.vote', name='vote'),
	url(r'^ajax/sticking/(?P<class_id>\d+)/(?P<item>\d+)/(?P<item_id>\d+)/?$', 'web.views.ajax.sticky_content', name='sticky'),
	url(r'^ajax/delete/(?P<item>\d+)/(?P<item_id>\d+)/?$', 'web.views.ajax.delete_content', name='delete_content'),
	                    
    url(r'^submit/(?P<sid>\d+)?/?$', 'web.views.submission.index', name='submit'),
	url(r'^expo_submit/(?P<eid>\d+)?/?$', 'web.views.submission.exposition', name='expo_submit'),
	url(r'^note_submit/(?P<nid>\d+)?/?$', 'web.views.submission.note_submit', name='note_submit'),
	url(r'^example_submit/(?P<exid>\d+)?/?$', 'web.views.submission.example_submit', name='example_submit'),
	       

    url(r'^post/(?P<sid>\d+)/?$', 'web.views.home.post', name='post'),

    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/atom/(?P<atom_id>\d+)/(?P<bid>\d+)?/?$', 'web.views.home.atom', name='atom'),
    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/(?P<bid>\d+)?/?$', 'web.views.home.category', name = 'category'),
    url(r'^class/(?P<class_id>\d+)/(?P<bid>\d+)?/?$', 'web.views.home.classes', name='classes'),
    url(r'^class-index/(?P<bid>\d+)?/?$', 'web.views.home.class_index', name='class_index'),
    url(r'^category/(?P<cat_id>\d+)/(?P<bid>\d+)?/?$', 'web.views.home.base_category', name='base_category'),
    url(r'^category/(?P<cat_id>\d+)/atom/(?P<atom_id>\d+)/(?P<bid>\d+)?/?$', 'web.views.home.base_atom', name='base_atom'),
    url(r'^(?P<bid>\d+)?/?$', 'web.views.home.index', name='home'),

    url(r'^mu-25b8a55c-a9fee579-723dcc44-9782bfc2$', 'web.views.blitz.index'),
    url(r'^google3da26e317e8e8cda.html$', 'web.views.google_webmaster.index'),
)
