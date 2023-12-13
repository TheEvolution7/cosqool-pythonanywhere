from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from core.models import *
from django.urls import reverse
from django.utils.safestring import mark_safe


class Group(MPTTModel, TranslatableModel, BaseModel):
    objects = CategoryManager()

    translations = translations()

    parent = TreeForeignKey('self', on_delete=models.DO_NOTHING,
                            null=True, blank=True, related_name='children')
    
    # created_by = models.ForeignKey(
    #     'accounts.User', on_delete=models.DO_NOTHING, related_name='created_by_account_user')

    class MPTTMeta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class Gallery(TranslatableModel, BaseModel):
    translations = translations()

    groups = TreeManyToManyField(Group)
    tags = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Gallery")
        verbose_name_plural = _("Gallery")


class Image(TranslatableModel, BaseModel):
    translations = translations()

    gallery = models.ForeignKey(
        Gallery, on_delete=models.DO_NOTHING, related_name="gallery_images")
    tags = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Image")

    def __str__(self):
        if self.title:
            return f'{self.title}'
        return f'{self.gallery}'

    def get_url(self):
        return reverse(f'admin:{self._meta.app_label}_{self._meta.model_name}_change', args=[self.id])

    def image_preview(self):
        t = reverse('admin:albums_image_change', args=[self.id])
        if self.image:
            return mark_safe(f'<a class="symbol symbol-125px" href="{t}"><img src="{self.thumbnail.url}" class="mw-100" /></a>')
        else:
            return '(No image)'
