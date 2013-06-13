from django.conf.urls import *

urlpatterns = patterns('',
    url(r'add_question/?$', 'assignment.views.question.addQ', name='add_question'),
    url(r'(?P<pk>\d+)/question/(?P<id>\d+)/?$', 'assignment.views.questionInstance.detail', name='question_instance'),
    url(r'question/(?P<id>\d+)/?$', 'assignment.views.question.detail', name='question_detail'),
    url(r'question/create/?$', 'assignment.views.question.create', name='question'),
    url(r'question/form/?$', 'assignment.views.question.form', name='question'),
    url(r'question/?$', 'assignment.views.question.index', name='question'),
    
    url(r'students/?$', 'assignment.views.staff.viewStudent', name='view_student'),
    url(r'evaluate/?$', 'assignment.views.staff.metrics', name='metrics'),

    url(r'eval/?$', 'assignment.views.student.eval', name='eval'),
    url(r'save/?$', 'assignment.views.student.save', name='save'),
    url(r'grades/?$', 'assignment.views.student.grades', name='grades'),

    url(r'preview/?$', 'assignment.views.question.preview', name='preview'),
    url(r'assign/add/?$', 'assignment.views.assign.create', name='add_assignment'),
    url(r'assign/instantiate/?$', 'assignment.views.assign.instantiate', name='instantiate'),
    url(r'assign/?$', 'assignment.views.assign.assign', name='assign'),
    url(r'(?P<id>\d+)/?$', 'assignment.views.assign.detail', name='assignment_detail'),
    url(r'', 'assignment.views.assign.index', name='assignment'),

)