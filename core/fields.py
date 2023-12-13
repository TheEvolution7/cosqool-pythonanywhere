from django import forms
from django.db import models

from .widgets import CKEditorWidget


class Select2Field(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            "form_class": Select2FormField,
            "widget": CKEditorWidget
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Select2FormField(forms.CharField):
    widget = CKEditorWidget

    def __init__(
        self,
        *args,
        **kwargs
    ):
        kwargs["widget"] = self.widget()
        super().__init__(*args, **kwargs)
