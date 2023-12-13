from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings
from core.models import *
from core.fields import *
from .fields import *


class Setting(TranslatableModel):
    CHOICES = (
        ("text", "Text"),
        ("textarea", "TextArea"),
        ("richtext", "RichText"),
        ("image", "Image"),
        ("file", "File"),
        ("gallery", "Gallery"),
        ("url", "Url"),
    )
    
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), unique=True,
                              blank=True, max_length=255, allow_unicode=True),

        text=models.CharField(max_length=255, blank=True),
        textarea=models.TextField(blank=True),
        richtext=RichTextField(blank=True),

        url=models.URLField(blank=True),
    )

    file = models.FileField(upload_to="files/", blank=True)
    image = models.ImageField(upload_to="files/", blank=True)

    type = models.CharField(max_length=16, choices=CHOICES, default=CHOICES[0])

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    @property
    def value(self):
        return getattr(self, self.type, None)
    
    
    def __str__(self):
        return f"{self.title}"
