from email.policy import default
from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import *
from pages.models import Page

class Group(TranslatableModel, BaseModel):
    translations = translations()
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True, default=1)
    class Meta:
        verbose_name = _("Field Group")
        verbose_name_plural = _("Field Groups")

    def __str__(self):
        return f"{self.title}"


class Field(MPTTModel, TranslatableModel, BaseModel):
    objects = CategoryManager()

    translations = translations()

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="parent_children",
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    attributes = models.JSONField(_("attributes"), default=dict, blank=True)

    class MPTTMeta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")

    class Meta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")

    @property
    def children(self):
        return self.get_children().filter().order_by("translations__position")

    @property
    def file(self):
        if self.media:
            return self.media.url
        if self.image:
            return self.image.url
