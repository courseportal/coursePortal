from django.template.defaultfilters import register

@register.filter(name='in_dict')
def check_in(dict, index):
    return index in dict

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

#@register.filter(name='vote_up', vote_up)
        #def vote_up(value, user):
#value.vote_up(user)

#@register.filter(name='vote_down', vote_down)
        #def vote_down(value, user):
#value.vote_down(user)