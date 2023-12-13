import ast
from django.apps import apps
from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from core.admin import *

from django.template.response import TemplateResponse
from django.urls import path
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status
from .serializer import *

@admin.register(Setting)
class SettingAdmin(CoreAdmin, TranslatableAdmin):
    base_fieldsets = ((None, {
        'fields': ('title', 'slug', )
    }),)
    
    list_display = ['str_tag', 'type', 'action_tag']
    list_filter = []
    

