from django.conf.urls import *

urlpatterns = patterns('',
    url(r'utility/matchType/?$', 'assignment.views.utility.matchType', name='matchType'),
    url(r'utility/validate/?$', 'assignment.views.utility.validate', name='validateVariable'),
    url(r'utility/validateFull/?$', 'assignment.views.utility.validateFull', name='validateFull'),
    url(r'utility/getTypeCode/?$', 'assignment.views.utility.getTypeCode', name='getTypeCode'),
    url(r'utility/practiceEval/?$', 'assignment.views.utility.practiceEval', name='practiceEval'),
    url(r'utility/reportQ/?$', 'assignment.views.utility.reportQ', name='reportQ'),

    url(r'add_question/?$', 'assignment.views.question.addQ', name='add_question'),
    url(r'(?P<pk>\d+)/question/(?P<id>\d+)/?$', 'assignment.views.question.instanceDetail', name='question_instance'),
    url(r'question/(?P<id>\d+)/?$', 'assignment.views.question.detail', name='question_detail'),
    url(r'question/preview/?$', 'assignment.views.question.preview', name='preview'),
    url(r'question/create/?$', 'assignment.views.question.create', name='create_question'),
    url(r'question/delete/(?P<id>\d+)?$', 'assignment.views.staff.deleteQ', name='delete_question'),
    url(r'question/list/?$', 'assignment.views.question.Qlist', name='question_list'),
    url(r'question/edit/(?P<id>\d+)?$', 'assignment.views.staff.editQ', name='edit_question'),

    url(r'delete/(?P<id>\d+)?$', 'assignment.views.staff.deleteA', name='delete_assignment'),
    url(r'qpreview/?$', 'assignment.views.staff.previewQuestion', name='preview_question'),
    url(r'preview/?$', 'assignment.views.staff.previewAssignment', name='preview_assignment'),
    url(r'preview/(?P<a>\d+)/?$', 'assignment.views.staff.previewTemplate', name='preview_assignment2'),
    url(r'students/(?P<id>\d+)?$', 'assignment.views.staff.viewStudent', name='view_student'),
    url(r'evaluate/?$', 'assignment.views.staff.metrics', name='metrics'),
    url(r'list/(?P<cid>\d+)', 'assignment.views.staff.csvList', name='csvList'),
    url(r'emailCSV/(?P<cid>\d+)/(?P<aid>\d+)?$', 'assignment.views.staff.emailCSV', name='csv'),

    url(r'eval/?$', 'assignment.views.student.eval', name='eval'),
    url(r'save/?$', 'assignment.views.student.save', name='save'),
    url(r'grades/?$', 'assignment.views.student.grades', name='grades'),
    url(r'student assignments/?$', 'assignment.views.student.list', name='list'),
    url(r'atom choice/?$', 'assignment.views.student.choose_atom', name='choose_practice_atom'),
    url(r'practice/(?P<id>\d+)?$', 'assignment.views.student.practice', name='practice'),
    
    url(r'extend/?$', 'assignment.views.staff.extend', name='extend'),
    url(r'select/(?P<c>\d+)?$', 'assignment.views.staff.selectInstance', name='select'),
    url(r'unmade/?$', 'assignment.views.assign.unmake', name='unmake'),
    url(r'unassign/(?P<c>\d+)?$', 'assignment.views.assign.unassign', name='unassign'),
    url(r'index/?$', 'assignment.views.assign.index', name='assignment_index'),
    url(r'create/?$', 'assignment.views.assign.create', name='create_assignment'),    
    url(r'add/?$', 'assignment.views.assign.addA', name='add_assignment'),
    url(r'list/?$', 'assignment.views.assign.Alist', name='assignment_list'),
    url(r'edit/(?P<id>\d+)/?$', 'assignment.views.assign.editA', name='edit_assignment'),
    url(r'instantiate/?$', 'assignment.views.assign.instantiate', name='instantiate'),
    url(r'assign/(?P<c>\d+)?$', 'assignment.views.assign.assign', name='assign'),
    url(r'(?P<id>\d+)/?$', 'assignment.views.assign.detail', name='assignment_detail'),
    url(r'', 'assignment.views.assign.main', name='assignment'),
)