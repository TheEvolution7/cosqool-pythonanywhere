from django.contrib import admin
from .models import *
from core.admin import *
# class SubscribedPlanInline(nested_admin.NestedTabularInline):
#     model = SubscribedPlan
#     extra = 0
@admin.register(Subscription)
class SubscriptionAdmin(nested_admin.NestedModelAdmin):
    pass
    # inlines = (SubscribedPlanInline, )
    
    # list_display = ['__str__', 'start_date', 'end_date', 'subscribed_plan_tag', 'action_tag']

    # @admin.display(description='Subscribed Plan')
    # def subscribed_plan_tag(self, obj):
    #     return obj.subscribed.all()
    
    # @admin.display(description='action')
    # def action_tag(self, obj):
    #     return action_tag(self, obj)

