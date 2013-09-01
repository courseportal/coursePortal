import autocomplete_light
autocomplete_light.autodiscover()

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from web import urls as web_urls
from assignment import urls as assignment_urls
from rating import urls as rating_urls
from haystack import urls as haystack_urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'vote/', include(rating_urls)),
    
    url(r'^ajax/bugReport/?$', 'knoatom.views.bug_report_view', name='bugReport'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^assignment/', include(assignment_urls)),
    url(r'^search/', include(haystack_urls)),
    url(r'autocomplete/', include('autocomplete_light.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^forum/', include('pybb.urls', namespace = 'pybb')),
    url(r'', include(web_urls)),
    # Uncomment the next line to enable the admin:
) + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))


