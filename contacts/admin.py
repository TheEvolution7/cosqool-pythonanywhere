from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import *
from core.admin import *


class MailInline(TranslatableStackedInline):
    model = Mail
    extra = 0
    fields = (('mail_to', 'mail_from'), ('subject',
              'additional_headers'), 'message_body', )


class MessageInline(TranslatableStackedInline):
    model = Message
    can_delete = False
    min_num = 1
    max_num = 1


def str_tag(self, obj):
    return mark_safe(f'<div class="text-start d-flex align-items-center"><a href="{obj.id}/change" class="symbol symbol-50px"><span class="symbol-label" style="background-image:url({obj.avatar});"></span></a><div class="ms-5"><a href="{obj.id}/change" class="text-gray-800 text-hover-primary fs-5 fw-bold">{truncatewords(obj,10)}</a> <span class="badge badge-primary">{obj.group}</span><div class="text-muted fs-7 fw-bold">{obj.email}</div></div></div>')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['str_tag', 'action_tag']

    @admin.display(description='action')
    def action_tag(self, obj):
        return action_tag(self, obj)

    @admin.display(description='name')
    def str_tag(self, obj):
        return str_tag(self, obj)

    fieldsets = (
        (None, {
            'fields': ('avatar', 'name', 'company', ('email', 'phone'), ('city', 'country'), 'note', )
        }),
        (_('Options'), {
            'fields': ('group', )
        }),
    )

@ admin.register(ContactForm)
class ContactFormAdmin(TranslatableAdmin):
    inlines = (MailInline, MessageInline, )

    list_display = ['str_tag', 'slug', 'action_tag']

    @admin.display(description='name')
    def str_tag(self, obj):
        return mark_safe(f'<div class="text-start d-flex align-items-center"><div class="ms-5"><a href="{obj.id}/change" class="text-gray-800 text-hover-primary fs-5 fw-bold">{truncatewords(obj,10)}</a><div class="text-muted fs-7 fw-bold"></div></div></div>')


    @ admin.display(description='action')
    def action_tag(self, obj):
        return action_tag(self, obj)

    fieldsets = (
        (None, {
            "fields": (
                ('title', 'slug'),
            ),
        }),
        (_('Status'), {
            "fields": (
                ('status',),
            ),
        }),
    )
    
@ admin.register(Group)
class GroupAdmin(TranslatableAdmin):
    list_display = ['str_tag', 'action_tag']

    @ admin.display(description='action')
    def action_tag(self, obj):
            return mark_safe(f'<div class="sweetalert"><div class="d-flex justify-content-end"><a href="{obj.id}/change" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Edit"><i class="fa fa-pencil"></i></a><a href="{obj.id}/delete" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Delete"><i class="fa fa-trash"></i></a></div></div>')


    @admin.display(description='name')
    def str_tag(self, obj):
        return mark_safe(f'<div class="text-start d-flex align-items-center"><div class="ms-5"><a href="{obj.id}/change" class="text-gray-800 text-hover-primary fs-5 fw-bold">{truncatewords(obj,10)}</a><div class="text-muted fs-7 fw-bold">{truncatewords(obj.description, 20)}</div></div></div>')

    
    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('title', ),
        }

    list_filter = ()
    
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'description', )
        }),
    )


