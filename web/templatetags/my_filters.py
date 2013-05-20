from django.template.defaultfilters import register

@register.filter(name='in_dict')
def check_in(dict, index):
    return index in dict

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''
