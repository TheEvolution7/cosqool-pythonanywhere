from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

from core.admin import *

    
@admin.register(ReportError)
class ReportErrorAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    list_filter = ()
    list_display = ['str_tag', 'content', 'updated_at', 'action_tag']
    base_fieldsets = (None, {
        'fields': ('content', )
    }),

    
