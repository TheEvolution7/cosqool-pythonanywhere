from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import *


class Group(TranslatableModel, BaseModel):

    translations = translations()

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Field Group")
        verbose_name_plural = _("Field Groups")

    def __str__(self):
        if self.content_object:
            return f'{self.content_object}: {self.title}'

        return f'{self.title}'


class Field(MPTTModel, TranslatableModel, BaseModel):
    objects = CategoryManager()

    translations = translations()

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='parent_children')
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, blank=True)
    attributes = models.JSONField(_('attributes'), default=dict, blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True, default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    class MPTTMeta:
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")

    @property
    def children(self):
        return self.get_children().filter().order_by('translations__position')

    @property
    def file(self):
        if self.media:
            return self.media.url
        if self.image:
            return self.thumbnail.url
