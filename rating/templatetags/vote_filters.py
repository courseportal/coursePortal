from django.template.defaultfilters import register

@register.filter    
def total(value, atom=None):
    return value.total(atom)