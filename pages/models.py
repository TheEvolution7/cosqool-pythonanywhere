from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel
from core.models import *


class Page(TranslatableModel, BaseModel):
    translations = translations()
    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')
