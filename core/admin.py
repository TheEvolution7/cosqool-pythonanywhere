from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableStackedInline, TranslatableTabularInline
from parler.forms import TranslatableModelForm
from imagekit.admin import AdminThumbnail
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse, path
from django.http import JsonResponse
from django.template.defaultfilters import truncatewords
import nested_admin
from django.template.loader import render_to_string


def action_tag(self, obj):
    return mark_safe(render_to_string('admin/tags/action_tag.html', {'obj': obj}))


def status_tag(self, obj):
    status = 'danger'
    if obj.status:
        status = 'primary'
        
    return mark_safe(f'<div class="badge badge-light-{status}">{obj.status}</div>')


def str_tag(self, obj):
    return mark_safe(render_to_string('admin/tags/str_tag.html', {'obj': obj}))


def fs_base():
    return ((None, {
        'fields': ('title', 'slug', 'description', 'content', )
    }),)


def fs_image():
    return ((_('Featured Image'), {
        'fields': ('image', ),
        'classes': ('show', )
    }),)


def fs_option():
    return ((_('Options'), {
        'fields': (('status', 'position'), 'media', ),
        'classes': ('show', )
    }),)


def fs_parent():
    return ((_('Parent'), {
        'fields': ('parent', ),
        'classes': ('show', )
    }),)


def fs_contenttypes():
    return (
        (_('Content Types'), {
            'fields': ('content_type', 'object_id', ),
        }),
    )


def get_object_id_choices(content_type_id):
    content_type = ContentType.objects.get_for_id(content_type_id)
    model_class = content_type.model_class()
    object_id_choices = [] or model_class.objects.all().values_list('pk',
                                                                    'translations__title')
    return object_id_choices

class SelectWidget(forms.Select):
    class Media:
        js = ["tests.js"]
        
class CustomSelect(SelectWidget):
    pass

class CoreForm(forms.Form):
    class Meta:
        widgets = {
            # "status": forms.Select(attrs={"data-control": "select2"}),
            "subject": forms.Select(attrs={"data-control": "select2"}),
            "parent": forms.Select(attrs={"data-control": "select2"}),
            "categories": forms.Select(attrs={"data-control": "select2", "multiple": "multiple"}),
            "tags": forms.Select(attrs={"data-control": "select2", "multiple": "multiple"}),
        }
        
class CoreBaseForm(CoreForm, TranslatableModelForm):
    pass

class BaseCoreAdmin(admin.ModelAdmin):
    # list_display = ['str_tag', 'action_tag']
    @admin.display(description='actions')
    def action_tag(self, obj):
        return action_tag(self, obj)

    @admin.display(description="")
    def str_tag(self, obj):
        return str_tag(self, obj)
    
    base_fieldsets = None
    
    extra_fieldset_title = _("Options")
    base_form = None

    def get_form(self, request, obj=None, **kwargs):
        # The django admin validation requires the form to have a 'class Meta: model = ..'
        # attribute, or it will complain that the fields are missing.
        # However, this enforces all derived ModelAdmin classes to redefine the model as well,
        # because they need to explicitly set the model again - it will stick with the base model.
        #
        # Instead, pass the form unchecked here, because the standard ModelForm will just work.
        # If the derived class sets the model explicitly, respect that setting.
        kwargs.setdefault("form", self.base_form or self.form)

        # prevent infinite recursion when this is called from get_subclass_fields
        if not self.fieldsets and not self.fields:
            kwargs.setdefault("fields", "__all__")

        return super().get_form(request, obj, **kwargs)

    def get_base_fieldsets(self, request, obj=None):
        return self.base_fieldsets

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = self.get_base_fieldsets(request, obj)

        # If subclass declares fieldsets or fields, this is respected
        if self.fieldsets or self.fields or not self.base_fieldsets:
            return super().get_fieldsets(request, obj)

        # Have a reasonable default fieldsets,
        # where the subclass fields are automatically included.
        other_fields = self.get_subclass_fields(request, obj)

        if other_fields:
            return (
                base_fieldsets[0],
            ) + base_fieldsets[1:] + ((self.extra_fieldset_title, {"fields": other_fields, "classes": ('show', )}),)
        else:
            return base_fieldsets

    def get_subclass_fields(self, request, obj=None):
        # Find out how many fields would really be on the form,
        # if it weren't restricted by declared fields.
        exclude = list(self.exclude or [])
        exclude.extend(self.get_readonly_fields(request, obj))

        # By not declaring the fields/form in the base class,
        # get_form() will populate the form with all available fields.
        form = self.get_form(request, obj, exclude=exclude)
        subclass_fields = list(form.base_fields.keys()) + list(
            self.get_readonly_fields(request, obj)
        )

        # Find which fields are not part of the common fields.
        for fieldset in self.get_base_fieldsets(request, obj):
            for field in fieldset[1]["fields"]:
                try:
                    subclass_fields.remove(field)
                except ValueError:
                    # field not found in form, Django will raise exception later.
                    pass
        return subclass_fields


from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin    
class CoreAdmin(BaseCoreAdmin, ImportExportModelAdmin, ExportActionModelAdmin, nested_admin.NestedModelAdmin, TranslatableAdmin):
    form = CoreBaseForm
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title', ),
        }
    list_filter = ('status', )
    search_fields = ['translations__title', 'id',
                     'translations__slug', 'translations__description']
    list_display = ['str_tag', 'slug', 'status_tag', 'updated_at', 'action_tag']

    @admin.display(description='status')
    def status_tag(self, obj):
        return status_tag(self, obj)
    
    
    
    
    base_fieldsets = fs_base() + fs_image()

    
def str_cat_tag(self, obj, ms):
    return mark_safe(f'<div class="d-flex align-items-center justify-content-start" style="margin-left: {ms}px;"><a href="{obj.id}/change" class="symbol symbol-50px"><span class="symbol-label" style="background-image:url({obj.thumbnail.url});"></span></a><div class="ms-5"><a href="{obj.id}/change" class="text-gray-800 text-hover-primary fs-5 fw-bold">{obj.title}</a> <span class="badge badge-primary">{obj.status.capitalize()}</span><div class="text-muted fs-7 fw-bold">{obj.description}</div></div></div>')


class CoreCategoryAdmin(CoreAdmin, TranslatableAdmin, MPTTModelAdmin):
    form = CoreBaseForm
    mptt_indent_field = "str_tag"
    mptt_level_indent = 50
    
class TabularInline(nested_admin.NestedStackedInline, TranslatableStackedInline):
    extra = 0
    form = CoreBaseForm
    