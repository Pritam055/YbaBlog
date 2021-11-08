from django import template
register = template.Library()

@register.filter(name="content_cut")
def cut(value, arg):
    # print(value, arg)
    
    return value[:arg] 