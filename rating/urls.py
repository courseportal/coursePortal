from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^ajax/([\w]+)/(\d+)/(\w+)/?$', 'rating.views.voteGeneral', name='voteGeneral'),
    url(r'^ajax/(\d+)/([\w]+)/(\d+)/(\w+)/?$', 'rating.views.vote', name='vote'),
)               
