from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^question/(?P<id>\d+)/?$', 'assignment.views.question.detail', name='question_detail'),
    url(r'^question/?$', 'assignment.views.question.index', name='question'),
    url(r'', 'assignment.views.assign.index', name='assignment'),
)
