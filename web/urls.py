from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login/?$', 'web.views.account.login', name='login'),
    url(r'^logout/?$', 'web.views.account.logout', name='logout'),
    url(r'^register/?$', 'web.views.account.register', name='register'),
    url(r'^validate/$', 'web.views.account.validate', name='validate'),
    url(r'^forgot_password/?$', 'web.views.account.forgot_password', name='forgot_password'),
    url(r'^account/?$', 'web.views.account.index', name='account'),

    url(r'^batch_add/?$', 'web.views.admin.batch_add', name='batch_add'),
    url(r'^view_videos/?$', 'web.views.admin.list_videos', name='list_videos'),

    url(r'^ajax/vote/(\d+)/(\d+)/(\d+)/?$', 'web.views.ajax.vote', name='vote'),

    #questions
    url(r'^question/(?P<id>\d+)/?$', 'web.views.question.detail', name='question_detail'),
    url(r'^question/?$', 'web.views.question.index', name='question'),

    url(r'^class/(?P<class_id>\d+)/submit/(?P<sid>\d+)?/?$', 'web.views.submission.index', name='submit'),
                    
    #LectureNote
    url(r'^media/file/(?P<filename>\w+\.pdf)$', 'web.views.LectureSubmit.display',name='LectureNoteDisplay'),
    url(r'^class/(?P<class_id>\d+)/submit/LectureNoteUpload/?$', 'web.views.LectureSubmit.index', name='LectureNoteUpload'),
                       
    url(r'^class/(?P<class_id>\d+)/post/(?P<sid>\d+)/?$', 'web.views.home.post', name='post'),
    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/atom/(?P<atom_id>\d+)/?$', 'web.views.home.atom', name='atom'),
    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/$', 'web.views.home.category', name = 'category'),
    url(r'^class/(?P<class_id>\d+)/$', 'web.views.home.classes', name='classes'),
    url(r'^$', 'web.views.home.index', name='home'),

    url(r'^mu-25b8a55c-a9fee579-723dcc44-9782bfc2$', 'web.views.blitz.index'),
    url(r'^google3da26e317e8e8cda.html$', 'web.views.google_webmaster.index'),
)
