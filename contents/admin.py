from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
from .models import *
import nested_admin

# The common admin functionality for all derived models:

class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    base_model = Field
    base_fieldsets = (
        GENERAL_FIELDSET,
    )
    
class FieldAdminInline(nested_admin.NestedStackedPolymorphicInline):
    model = Field
    
    class CategoryInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = Category
    
    class TextInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = Text
    
    class ImageInline(nested_admin.NestedStackedPolymorphicInline.Child):
        model = Image

    child_inlines = (CategoryInline, TextInline, ImageInline, )
    
@admin.register(FieldGroup)
class FieldGroupAdmin(nested_admin.NestedPolymorphicModelAdmin):
    inlines = (FieldAdminInline, )
    
@admin.register(Field)
class FieldAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = Field
    child_models = (
        Category,
        Text,
        Image,
    )

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }
        
@admin.register(Text)
class TextAdmin(BaseChildAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(BaseChildAdmin):
    pass

@admin.register(Image)
class ImageAdmin(BaseChildAdmin):
    pass