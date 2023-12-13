from django import template
from ..models import *

register = template.Library()

@register.inclusion_tag('notification.html', takes_context=True)
def notification(context):
    
    return context