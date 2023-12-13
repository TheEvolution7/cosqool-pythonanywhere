from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _

from core.admin import *

class MenuItemAdminInline(nested_admin.NestedStackedInline, TranslatableStackedInline):
    model = MenuItem
    extra = 0
    sortable_field_name = "position"

    
@admin.register(Menu)
class MenuAdmin(CoreAdmin):
    fieldsets = ((None, {
        'fields': (('title', 'slug'), )
    }),)

    # inlines = [MenuItemAdminInline]
    
@admin.register(MenuItem)
class MenuItemAdmin(CoreCategoryAdmin):
    pass
    
