from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_enrollment(context):
    return 1