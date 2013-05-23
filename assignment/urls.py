from django.conf.urls import *
from assignment import views

urlpatterns = patterns('',
    url(r'', 'assignment.views.index', name='question'),
    url(r'^question/(?P<id>\d+)/?$', 'assignment.views.detail', name='question_detail'),
    url(r'^question/?$', 'assignment.views.index', name='question'),
)
