from django.template.defaultfilters import register

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
    return value.totalUp(atom)/(value.totalUp(atom)+value.totalDown(atom))*100

@register.filter(name="totalDownPercentage")
def totalDownPercentage(value, atom=None):
    return value.totalDown(atom)/(value.totalUp(atom)+value.totalDown(atom))*100