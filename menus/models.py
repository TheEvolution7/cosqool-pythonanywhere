from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.models import *
from django.urls import reverse
from pages.models import *


class Menu(TranslatableModel, BaseModel):

    translations = translations()

    class Meta:
        ordering = ("pk",)
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

class MenuItem(MPTTModel, TranslatableModel, BaseModel):
    objects = CategoryManager()

    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), blank=True, allow_unicode=True),
        description=models.TextField(
            _('description'), null=True, blank=True),
        content=RichTextUploadingField(
            _('content'), null=True, blank=True),
        position = models.IntegerField(_('Position'), null=True, default=0)
    )

    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    menu = models.ForeignKey(Menu, related_name="items",
                             on_delete=models.CASCADE)

    url = models.URLField(max_length=256, blank=True, null=True)

    # objects = models.Manager()
    tree = TreeManager()

    page = models.ForeignKey(
        Page, blank=True, null=True, on_delete=models.CASCADE)

    class MPTTMeta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    class Meta:
        ordering = ("translations__position", "pk")
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def children(self):
        return self.get_children().filter()

    def get_absolute_url(self):
        if self.slug == 'home':
            return "/dashboards/"
        return "/dashboards" + '/' + self.slug
        return reverse("dashboards:details", kwargs={"slug": self.slug})
    
    @property
    def linked_object(self):
        return  self.page
    # @property
    # def get_url(self):
    #     if self.url:
    #         return self.url

    #     if self.content_object:
    #         if self.content_object.id != 1:
    #             return reverse(f'frontend:page-detail', args=[self.content_object.slug])
    #         return reverse(f'frontend:home')

    #     return '#'
