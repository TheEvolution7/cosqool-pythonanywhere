from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class File(models.Model):
    file = models.FileField(
        _("file"),
        null=True,
        blank=True,
        max_length=255,
    )
    name = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name=_("name"),
    )

    description = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("description"),
    )

    owner = models.ForeignKey(
        getattr(settings, 'AUTH_USER_MODEL', 'auth.User'),
        # related_name='owned_%(class)ss',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("owner"),
    )

    created_at = models.DateTimeField(
        _("uploaded at"),
        auto_now_add=True,
    )

    modified_at = models.DateTimeField(
        _("modified at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("file")
        verbose_name_plural = _("files")

    @property
    def get_url(self):
        return self.file.url
