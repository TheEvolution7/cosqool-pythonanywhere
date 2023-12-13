# from django.contrib import admin
# from .models import *
# from django.utils.translation import gettext_lazy as _
# from core.admin import *

# class PriceInline(nested_admin.NestedTabularInline, TranslatableTabularInline):
#     model = Price
#     fields = ('title', 'price_amount', 'currency', )
#     extra = 0
    
# @admin.register(Plan)
# class PlanAdmin(CoreAdmin):
#     inlines = (PriceInline, )
#     list_display = ['str_tag', 'price_tags', 'status_tag', 'created_at','action_tag']
    
#     @admin.display(description='Price')
#     def price_tags(self, obj):
#         return f"{obj.get_price_default().price_amount} {obj.get_price_default().currency}"
    
#     @admin.display(description='Status')
#     def status_tag(self, obj):
#         return mark_safe(f'{status_tag(obj)}')
    



