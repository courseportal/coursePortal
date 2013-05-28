from django.conf.urls import *

urlpatterns = patterns('',
    url(r'[0-9]+/question/(?P<id>\d+)/?$', 'assignment.views.questionInstance.detail', name='question_instance'),
    url(r'question/(?P<id>\d+)/?$', 'assignment.views.question.detail', name='question_detail'),
    url(r'question/?$', 'assignment.views.question.index', name='question'),
    
    url(r'assign/instantiate/?$', 'assignment.views.assign.instantiate', name='instantiate'),
    url(r'assign/?$', 'assignment.views.assign.assign', name='assign'),
    url(r'(?P<id>\d+)/?$', 'assignment.views.assign.detail', name='assignment_detail'),
    url(r'', 'assignment.views.assign.index', name='assignment'),
)
