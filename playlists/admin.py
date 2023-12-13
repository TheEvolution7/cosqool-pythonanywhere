from django.utils.translation import gettext_lazy as _
from .models import Playlist, PlaylistItem
from core.admin import admin, BaseCoreAdmin
import nested_admin

class PlaylistItemInline(nested_admin.NestedTabularInline):
    model = PlaylistItem
    extra = 0
    
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin

class PlaylistResource(resources.ModelResource):

    class Meta:
        model = Playlist
        
# @admin.register(Playlist)
# class PlaylistAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin, ExportActionModelAdmin, ImportExportModelAdmin):
#     resource_classes = [PlaylistResource]
#     base_fieldsets = (
#         (None, {
#             'fields': ('title', 'description', )
#         }),
#     )
#     inlines = (PlaylistItemInline, )

