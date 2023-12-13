from django.contrib import admin
from .models import *
from core.admin import *

class BillingItemAdmin(nested_admin.NestedTabularInline):
    model = BillingItem
    extra = 0
    max_num = 1
    
@admin.register(Billing)
class BillingAdmin(BaseCoreAdmin, nested_admin.NestedModelAdmin):
    base_fieldsets = ((None, {
        'fields': ('description', )
    }),)
    inlines = (BillingItemAdmin, )

