from django.template.defaultfilters import register

@register.filter    
def total(value, atom=None):
    return value.total(atom)

@register.filter   
def totalUp(value, atom=None):
    return value.totalUp(atom)

@register.filter   
def totalDown(value, atom=None):
    return value.totalDown(atom)