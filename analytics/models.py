from django.db import models
from django.utils.translation import gettext_lazy as _

class Overview(models.Model):
    class Meta:
        verbose_name = _(" Overview")
        verbose_name_plural = _(" Overview")

class Product(models.Model):
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

class Variation(models.Model):
    class Meta:
        verbose_name = _("Variation")
        verbose_name_plural = _("Variations")

class Order(models.Model):
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

class Revenue(models.Model):
    class Meta:
        verbose_name = _("Revenue")
        verbose_name_plural = _("Revenue")

class Download(models.Model):
    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")