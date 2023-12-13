from django import template
from ..models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def linklists(context, menu):
    menuitems = MenuItem.objects.filter(status=True, menu__translations__slug=menu).all()
    return menuitems