from django import template

register = template.Library()

@register.filter(name="addclass")
def addclass(value, class_name):
    value.field.widget.attrs["class"] = class_name
    return value