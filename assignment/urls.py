from django.conf.urls import *

urlpatterns = patterns('',
    url(r'utility/checktitle/?$', 'assignment.views.utility.checkAssignmentTitle', name='check_title'),

    url(r'add_question/?$', 'assignment.views.question.addQ', name='add_question'),
    url(r'(?P<pk>\d+)/question/(?P<id>\d+)/?$', 'assignment.views.question.instanceDetail', name='question_instance'),
    url(r'question/preview/?$', 'assignment.views.question.preview', name='preview'),
    url(r'question/create/?$', 'assignment.views.question.create', name='create_question'),
    url(r'question/delete/?$', 'assignment.views.staff.deleteQ', name='delete_question'),
    
    url(r'delete/?$', 'assignment.views.staff.deleteA', name='delete_assignment'),
    url(r'qpreview/?$', 'assignment.views.staff.previewQuestion', name='preview_question'),
    url(r'preview/?$', 'assignment.views.staff.previewAssignment', name='preview_assignment'),
    url(r'preview/(?P<a>\d+)/?$', 'assignment.views.staff.previewTemplate', name='preview_assignment2'),
    url(r'students/?$', 'assignment.views.staff.viewStudent', name='view_student'),
    url(r'evaluate/?$', 'assignment.views.staff.metrics', name='metrics'),

    url(r'eval/?$', 'assignment.views.student.eval', name='eval'),
    url(r'save/?$', 'assignment.views.student.save', name='save'),
    url(r'grades/?$', 'assignment.views.student.grades', name='grades'),
    url(r'list/?$', 'assignment.views.student.list', name='list'),
    
    url(r'unmade/?$', 'assignment.views.assign.unmake', name='unmake'),
    url(r'unassign/?$', 'assignment.views.assign.unassign', name='unassign'),
    url(r'index/?$', 'assignment.views.assign.index', name='assignment_index'),
    url(r'create/?$', 'assignment.views.assign.create', name='create_assignment'),    
    url(r'add/?$', 'assignment.views.assign.addA', name='add_assignment'),
    url(r'edit/(?P<id>\d+)/?$', 'assignment.views.assign.editA', name='edit_assignment'),
    url(r'instantiate/?$', 'assignment.views.assign.instantiate', name='instantiate'),
    url(r'assign/?$', 'assignment.views.assign.assign', name='assign'),
    url(r'(?P<id>\d+)/?$', 'assignment.views.assign.detail', name='assignment_detail'),
    url(r'', 'assignment.views.assign.main', name='assignment'),
)