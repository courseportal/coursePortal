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