from email.policy import default
from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from core.models import *
from django.conf import settings

class ArticleCategory(BaseModel, MPTTModel):
    title=models.CharField(_('title'), max_length=255)
    slug=models.SlugField(_('slug'), unique=True, blank=True, max_length=255, allow_unicode=True)
    description=models.TextField(
        _('description'), null=True, blank=True)
    content=RichTextUploadingField(
        _('content'), null=True, blank=True)
    position = models.IntegerField(_('Position'), null=True, default=0)

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, default=None)

    class MPTTMeta:
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")

    class Meta:
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")

    def get_last_article(self):
        return Article.objects.filter().order_by('-id').all()
    
    def articles(self):
        return self.article_set.filter().all()

    def children(self):
        return self.get_children().filter()

class Tag(BaseModel):
    title=models.CharField(_('title'), max_length=255)
    slug=models.SlugField(_('slug'), unique=True, blank=True, max_length=255, allow_unicode=True)
    description=models.TextField(
        _('description'), null=True, blank=True)
    content=RichTextUploadingField(
        _('content'), null=True, blank=True)
    position = models.IntegerField(_('Position'), null=True, default=0)
    
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
    
    def articles(self):
        return self.article_set.filter().all()
    
class Article(BaseModel):
    title=models.CharField(_('title'), max_length=255)
    slug=models.SlugField(_('slug'), unique=True, blank=True, max_length=255, allow_unicode=True)
    description=models.TextField(
        _('description'), null=True, blank=True)
    content=RichTextUploadingField(
        _('content'), null=True, blank=True)
    position = models.IntegerField(_('Position'), null=True, default=0)

    categories = TreeManyToManyField(ArticleCategory)
    # tags = models.TextField(null=True, blank=True)
    
    tags = models.ManyToManyField(Tag, blank=True)
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        default=1
    )
    
    def get_first_category(self):
        return self.categories.filter().first()
    
    def get_category_list(self):
        return self.categories.filter().all()
    
    def get_tags(self):
        return self.tags.filter().all()
    
    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['-id']
