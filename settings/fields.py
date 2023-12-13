from typing import Any
from django import forms
from django.db import models

from .widgets import *
from django.contrib.admin import site as admin_site

class ImagePickerField(models.ForeignKey):
    
    def formfield(self, **kwargs):
        defaults = {
            'widget': ImagePickerWidget
        }
        defaults.update(kwargs)
        formfield = super().formfield(**defaults)
        formfield.queryset = self.related_model.objects.order_by("-pk")
        return formfield

class ImagePickerMultipleField(models.ManyToManyField):
    
    def formfield(self, **kwargs):
        defaults = {
            'widget': ImagePickerMultipleWidget
        }
        defaults.update(kwargs)
        formfield = super().formfield(**defaults)
        # formfield.widget = ImagePickerMultipleWidget(
        #     formfield.widget,
        #     self.remote_field,
        # )
        formfield.queryset = self.related_model.objects.order_by("-pk")
        return formfield