from django.conf import settings
from django.conf.urls import patterns, include, url
from web.views.edit_class import CreateClassView

urlpatterns = patterns('',
    url(r'^login/?$', 'web.views.account.login', name='login'),
    url(r'^logout/?', 'web.views.account.logout', name='logout'),
    url(r'^register/?$', 'web.views.account.register', name='register'),
    url(r'^validate/?$', 'web.views.account.validate', name='validate'),
    url(r'^forgot-password/?$', 'web.views.account.forgot_password', name='forgot_password'),
    url(r'^account/?$', 'web.views.account.index', name='account'),

    url(r'^batch-add/?$', 'web.views.admin.batch_add', name='batch_add'),

	url(r'^ajax/report/?$', 'web.views.home.report', name="report"),
	                    
    url(r'^submit-content/(?P<pk>\d+)?/?$', 
        'web.views.submission.submit_content', name="submit_content"),
    url(r'^delete-content/?$', 'web.views.submission.delete_content', 
        name="delete_content"),
    url(r'^content/(?P<pk>\d+)/?$', 'web.views.home.content_detail', 
        name="content_details"),
#    url(r'^base-category/(?P<cat_id>\d+)?/content/(?P<pk>\d+)/?$', 'web.views.home.content_detail', name="cat_content_details"),
#     url(r'^base-category/(?P<cat_id>\d+)?/atom/(?P<atom_id>\d+)?/content/(?P<pk>\d+)/?$', 'web.views.home.content_detail', name="atom_content_details"),
#     url(r'^class/(?P<class_id>\d+)?/category/(?P<cat_id>\d+)?/content/(?P<pk>\d+)/?$', 'web.views.home.content_detail', name="class_cat_content_details"),
#     url(r'^class/(?P<class_id>\d+)?/category/(?P<cat_id>\d+)?/atom/(?P<atom_id>\d+)?/content/(?P<pk>\d+)/?$', 'web.views.home.content_detail',
#         name="class_atom_content_details"),
	 
	# URLs for the class editing form
	url(r'^create-class/?$', CreateClassView.as_view(), name='create_class'),
	url(r'^edit-class/(?P<class_id>\d+)/(?P<cat_id>\d+)?/?$', 'web.views.edit_class.EditClassView', name='edit_class'),
	# URLs for class editing form that are ONLY used with AJAX
	url(r'^ajax/get-children/(?P<is_class>\d+)/(?P<pk>\d+)?/?$', 'web.views.edit_class.get_children', name='get_children'),
    url(r'^ajax/delete-class/(?P<pk>\d+)/?$', 'web.views.edit_class.delete_class', name="delete_class"),
	url(r'^ajax/delete-category/(?P<pk>\d+)/?$', 'web.views.edit_class.delete_category', name="delete_category"),
    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/atom/(?P<atom_id>\d+)/?$', 'web.views.home.atom', name='atom'),
    url(r'^class/(?P<class_id>\d+)/category/(?P<cat_id>\d+)/?$', 'web.views.home.category', name = 'category'),
    url(r'^class/(?P<class_id>\d+)/?$', 'web.views.home.classes', name='classes'),
    url(r'^class-index/?$', 'web.views.home.class_list', name='class_index'),
    url(r'^base-category/(?P<cat_id>\d+)/?$', 'web.views.home.category', name='base_category'),
    url(r'^base-category/(?P<cat_id>\d+)/atom/(?P<atom_id>\d+)/?$', 'web.views.home.atom', name='base_atom'),
    url(r'^/?$', 'web.views.home.index', name='home'),

    url(r'^mu-25b8a55c-a9fee579-723dcc44-9782bfc2$', 'web.views.blitz.index'),
    url(r'^google3da26e317e8e8cda.html$', 'web.views.google_webmaster.index'),
)
