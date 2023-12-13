# from django.db import models
# from parler.models import TranslatableModel
# from django.utils.translation import gettext_lazy as _
# from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
# from core.models import *

# from django_measurement.models import MeasurementField
# from django_prices.models import MoneyField
# from measurement.measures import Weight
# from django.core.validators import MinValueValidator
# from django.conf import settings
# from django.urls import reverse
# from django.utils.safestring import mark_safe
# from courses.models import *
# # class Category(MPTTModel, TranslatableModel, BaseModel):
# #     translations = translations()
# #     objects = objects = CategoryManager()
# #     parent = TreeForeignKey('self', on_delete=models.CASCADE,
# #                             null=True, blank=True)

# #     class MPTTMeta:
# #         verbose_name = _("Category")
# #         verbose_name_plural = _("Categories")

# #     class Meta:
# #         verbose_name = _("Category")
# #         verbose_name_plural = _("Categories")


# class Plan(TranslatableModel, BaseModel):
#     translations = translations()
#     grades = models.ManyToManyField("courses.Grade", blank=True)
#     # tests = models.ManyToManyField(TestPrep, blank=True)

#     class Meta:
#         verbose_name = _("Plan")
#         verbose_name_plural = _("Plans")
    
#     def get_course_list(self):
#         return self.grades.filter().all()
    
#     def get_test_list(self):
#         return self.tests.filter().all()
    
#     def get_price_default(self):
#         return self.price_set.filter().first()
    
#     def get_price_list(self):
#         return self.price_set.filter().all()


# class Price(TranslatableModel):
#     translations = TranslatedFields(
#         title=models.CharField(_('title'), max_length=255),
#     )
#     plan = models.ForeignKey(
#         Plan, on_delete=models.CASCADE
#     )
#     currency = models.CharField(
#         max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH, default='USD')
#     price_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         default=0.0
#     )
#     price = MoneyField(amount_field="price_amount", currency_field="currency")

#     def __str__(self):
#         return self.title
#     class Meta:
#         verbose_name = _("Price")
#         verbose_name_plural = _("Prices")
