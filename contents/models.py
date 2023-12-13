from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class FieldGroup(models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    title = models.CharField(_("Title"), max_length=200)
    def __str__(self):
        return self.title


class Field(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey(
        'self', blank=True, null=True, related_name='children', verbose_name=_('parent'), on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=200)

    field_group = models.ForeignKey(
        FieldGroup, on_delete=models.CASCADE)

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = _("Field")
        verbose_name_plural = _("Fields")
    
    def __str__(self):
        return self.title


class Category(Field):
    opening_title = models.CharField(_("Opening title"), max_length=200)
    opening_image = models.ImageField(_("Opening image"), upload_to='images')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Text(Field):
    extra_text = models.TextField()
    can_have_children = False

    class Meta:
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")


class Image(Field):
    images = models.ImageField(_("Image"), upload_to='images')

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")
