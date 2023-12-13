from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

from parler.models import TranslatedFields
from django.utils.translation import gettext_lazy as _
from mptt.managers import TreeManager, TreeQuerySet
from parler.managers import TranslatableQuerySet, TranslatableManager
from django.utils.text import slugify, capfirst
from imagekit.models import ImageSpecField
from django.utils.html import strip_tags
from imagekit.processors import ResizeToFill

from parler.models import TranslatableModel

class CategoryQuerySet(TranslatableQuerySet, TreeQuerySet):
    
    def as_manager(cls):
        manager = CategoryManager.from_queryset(cls)()
        manager._built_with_as_manager = True
        return manager
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


class CategoryManager(TreeManager, TranslatableManager):
    _queryset_class = CategoryQuerySet

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)
    
class CustomManager(TreeManager, TranslatableManager):
    def manager_only_method(self):
        return


class CustomQuerySet(TranslatableQuerySet):
    def manager_and_queryset_method(self):
        return

import uuid

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    image = models.ImageField(_('image'),
                              upload_to='%(class)s/', null=True, blank=True)
    thumbnail = ImageSpecField(
        source='image', processors=[ResizeToFill(150, 150)] ,format='WEBP')
    
    medium = ImageSpecField(
        source='image', processors=[ResizeToFill(300, 300)] ,format='WEBP')

    large = ImageSpecField(
        source='image', processors=[ResizeToFill(1024, 1024)] ,format='WEBP')
    
    media = models.FileField(_('media'),
                             upload_to='%(class)s/', null=True, blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    
    STATUS_CHOICES = [
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if hasattr(self, 'title'):
            self.title = capfirst(strip_tags(self.title))
        if hasattr(self, 'description'):
            self.description = capfirst(strip_tags(self.description))
        if hasattr(self, 'slug') and not self.slug and self.id != 1:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    

    def __str__(self):
        from parler.models import TranslationDoesNotExist
        try:
            return self.title
        except TranslationDoesNotExist:
            return ''

    class Meta:
        # ordering = ["id"]
        abstract = True


def translations():
    return TranslatedFields(
        title=models.CharField(_('title'), max_length=255),
        slug=models.SlugField(_('slug'), unique=True, blank=True, max_length=255, allow_unicode=True),
        description=models.TextField(
            _('description'), null=True, blank=True),
        content=RichTextUploadingField(
            _('content'), null=True, blank=True),
        position = models.IntegerField(_('Position'), null=True, default=0)
    )
    
        
