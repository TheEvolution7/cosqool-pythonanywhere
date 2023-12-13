from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Page
from core.admin import *


@admin.register(Page)
class PageAdmin(CoreAdmin):
    pass
