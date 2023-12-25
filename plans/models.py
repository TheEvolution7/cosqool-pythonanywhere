from django.db import models
from parler.models import TranslatableModel
from django.utils.translation import gettext_lazy as _
from core.models import *

from django_prices.models import MoneyField
from django.conf import settings


class Plan(TranslatableModel, BaseModel):
    translations = translations()

    def get_plan_item(self):
        return self.plan_items.filter().all()

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")


class Option(TranslatableModel, BaseModel):
    translations = translations()

    class Meta:
        verbose_name = _("Option")
        verbose_name_plural = _("Options")


from courses.models import Grade
from testpreps.models import TestPrep


class PlanItem(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="items")
    grades = models.ManyToManyField(Grade, blank=True)
    testpreps = models.ManyToManyField("testpreps.TestPrep", blank=True, related_name="testpreps_planitems")
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True)
    paypal_plan_id = models.CharField(max_length=255, null=True, blank=True)
    amount = models.FloatField(default=0.0)
    currency = models.CharField(max_length=10, default="USD")

    def get_grades(self):
        return self.grades.filter(status=True).all()

    def get_testpreps(self):
        return self.testpreps.filter(status=True).all()

    def get_options(self):
        return self.option.title

    def get_prices(self):
        return self.prices.filter().all()

    def get_first_price(self):
        return self.prices.filter().first()


class Price(models.Model):
    plan_item = models.ForeignKey(
        PlanItem, on_delete=models.CASCADE, related_name="prices"
    )

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH, default="USD"
    )
    price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0.0,
    )
    price = MoneyField(amount_field="price_amount", currency_field="currency")

    class Meta:
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")
