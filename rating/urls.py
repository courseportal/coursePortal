from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^ajax/([a-z]+)/(\d+)/(\d+)/?$', 'rating.views.voteGeneral', name='voteGeneral'),
)               
