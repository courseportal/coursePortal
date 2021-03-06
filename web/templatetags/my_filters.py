from django.template.defaultfilters import register
from django.utils import simplejson as json

@register.filter(name='in_dict')
def check_in(dict, index):
    return index in dict

@register.filter(name='lookup')
def lookup(dict, index):
    if str(index) in dict:
        return dict[str(index)]
    return ''

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter(name="student_performance")
def performance(student):
	achieved=0.0
	possible=0.0
	for i in student.assignmentInstances.all():
		achieved+=i.score
		possible+=i.max_score
	if possible == 0.0:
		return "No Assignments"
	value = float((achieved/possible)*100)
	performance=str(value)+'%'
	return performance

@register.filter(name="has_atom")
def has_atom(qset, aid):
	try:
		return qset.filter(id=aid).exists()
	except:
		return False

@register.filter
def total(value, atom=None):
    return value.total(atom)

@register.filter(name="totalUp")
def totalUp(value, atom=None):
    return value.totalUp(atom)

@register.filter(name="totalDown")
def totalDown(value, atom=None):
    return value.totalDown(atom)

@register.filter(name="totalUpPercentage")
def totalUpPercentage(value, atom=None):
    if (value.totalUp(atom)+value.totalDown(atom)):
        return value.totalUp(atom)*100/(value.totalUp(atom)+value.totalDown(atom))
    else:
        return 50

@register.filter(name="totalDownPercentage")
def totalDownPercentage(value, atom=None):
    if (value.totalUp(atom)+value.totalDown(atom)):
        return value.totalDown(atom)*100/(value.totalUp(atom)+value.totalDown(atom))
    else:
        return 50