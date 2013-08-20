from django.template.defaultfilters import register
from django.utils import simplejson as json
from django import template

register = template.Library()

@register.simple_tag
def get_content_url(content, class_, category, atom):
    print('class: {}\ncategory: {}\natom: {}\n'.format(class_, category, atom))
    if class_ == "":
        class_ = None
    if category == "":
        category = None
    if atom == "":
        atom = None
    return content.get_absolute_url(class_, category, atom)

@register.filter(name='in_dict')
def check_in(dict, index):
    return index in dict

@register.filter(name='lookup')
def lookup(dict, index):
    if str(index) in dict:
        return dict[str(index)]
    return ''

@register.filter(name='index')
def index(l, index):
    if len(l) > int(index):
        return l[int(index)]
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

