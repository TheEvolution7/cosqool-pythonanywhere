from django.contrib import admin
from .models import *
from core.admin import *
from django.utils.translation import gettext_lazy as _

@admin.register(Group)
class GroupAdmin(CoreAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    
    list_display = ['str_tag', 'slug', 'content_type', 'status','fields_tag', 'action_tag']
    
    @admin.display(description='fields')
    def fields_tag(self, obj):
        return obj.field_set.count()

@admin.register(Field)
class FieldsAdmin(CoreCategoryAdmin, ImportExportModelAdmin, ExportActionModelAdmin):
    list_display = ['str_tag','group','action_tag']
    list_filter = ('status', 'group', )