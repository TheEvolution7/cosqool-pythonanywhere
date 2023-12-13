from django.contrib import admin
from .models import *
from core.admin import *

from import_export.admin import ImportExportModelAdmin
from import_export.admin import ExportActionModelAdmin
from .resources import *
@admin.register(Event)
class EventAdmin(BaseCoreAdmin):
    base_fieldsets = ((None, {
        'fields': ('content', )
    }),)
    search_fields = ('id', )
    resource_classes = [EventResource]
    

@admin.register(EventObject)
class EventObjectAdmin(BaseCoreAdmin):
    base_fieldsets = ((None, {
        'fields': ('content', )
    }),)

@admin.register(Calendar)
class CalendarAdmin(BaseCoreAdmin):
    base_fieldsets = ((None, {
        'fields': ('content', )
    }),)
