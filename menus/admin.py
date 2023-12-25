from django.contrib import admin
from .models import Menu, MenuItem

from core.admin import CoreAdmin, CoreCategoryAdmin


@admin.register(Menu)
class MenuAdmin(CoreAdmin):
    pass


@admin.register(MenuItem)
class MenuItemAdmin(CoreCategoryAdmin):
    list_display = ['__str__', 'slug', 'status_tag', 'updated_at', 'action_tag']
