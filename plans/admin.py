from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core.admin import *


class PlanItemInline(nested_admin.NestedTabularInline):
    model = PlanItem
    extra = 0


@admin.register(Plan)
class PlanAdmin(CoreAdmin):
    inlines = (PlanItemInline,)


@admin.register(Option)
class OptionAdmin(CoreAdmin):
    pass
