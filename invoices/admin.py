from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core.admin import *

class InvoiceEventInline(admin.TabularInline):
    model = InvoiceEvent
    extra = 0

def status_tag(obj):
    if obj.status == JobStatus.PENDING:
        status = 'primary'
    
    if obj.status == JobStatus.SUCCESS:
        status = 'success'
    
    if obj.status == JobStatus.FAILED:
        status = 'info'
        
    if obj.status == JobStatus.DELETED:
        status = 'danger'
    
    return mark_safe(f' <span class="badge badge-{status}">{obj.status.capitalize()}</span>')
        
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('str_tag', 'status_tag', 'total_tag','created', 'action_tag', )
    
    list_filter = ('status', )
    search_fields = ['number', 'id', ]
    
    @admin.display(description='action')
    def action_tag(self, obj):
        return action_tag(self, obj)
    
    @admin.display(description='Total')
    def total_tag(self, obj):
        return obj.subscription.get_billing_amount
            
    @admin.display(description='Status')
    def status_tag(self, obj):
        return mark_safe(f'{status_tag(obj)}')
    
    @admin.display(description='title')
    def str_tag(self, obj):
        return mark_safe(f'<div class="text-start d-flex align-items-center min-w-300px"><a href="{obj.id}/change" class="text-gray-800 text-hover-primary fs-5 fw-bold">{truncatewords(obj, 8)}</a><div class="text-muted fs-7 fw-bold"></div></div></div>')
    
    fieldsets = (
        (None, {
            'fields': (('subscription', 'number'), ('external_url', 'invoice_file'), 'message', )
        }),
        (_('Options'), {
            'fields': ('created', 'status', )
        }),
    )
    inlines=(InvoiceEventInline,)


@admin.register(InvoiceEvent)
class InvoiceEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'date',)
    
