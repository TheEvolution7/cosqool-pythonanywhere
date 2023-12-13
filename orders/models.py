from decimal import Decimal
from operator import attrgetter
from re import match
from typing import TYPE_CHECKING, List, Optional, cast
from uuid import uuid4

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import connection, models
from django.db.models import F, JSONField, Max
from django.db.models.expressions import Exists, OuterRef
from django.utils.timezone import now
# from sequences import get_next_value
from django_prices.models import MoneyField, TaxedMoneyField
from prices import Money, TaxedMoney

from typing import Iterable
from . import (
    FulfillmentStatus,
    OrderAuthorizeStatus,
    OrderChargeStatus,
    OrderEvents,
    OrderOrigin,
    OrderStatus,
)

from products.models import *

def zero_money(currency: str):
    return Money(0, currency)


def zero_taxed_money(currency: str):
    zero = zero_money(currency)
    return TaxedMoney(net=zero, gross=zero)


def get_subtotal(order_lines: Iterable["OrderLine"], fallback_currency: str):
    if not fallback_currency:
        fallback_currency = 'USD'
    subtotal_iterator = (line.total_price for line in order_lines)
    return sum(subtotal_iterator, zero_taxed_money(currency=fallback_currency))


class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,
                          unique=True, default=uuid4)
    # number = models.IntegerField(
    #     unique=True, default=get_next_value('orders'), editable=False)
    # use_old_id = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, db_index=True)
    status = models.CharField(
        max_length=32, default=OrderStatus.UNFULFILLED, choices=OrderStatus.CHOICES
    )
    authorize_status = models.CharField(
        max_length=32,
        default=OrderAuthorizeStatus.NONE,
        choices=OrderAuthorizeStatus.CHOICES,
        db_index=True,
    )
    charge_status = models.CharField(
        max_length=32,
        default=OrderChargeStatus.NONE,
        choices=OrderChargeStatus.CHOICES,
        db_index=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="orders",
        on_delete=models.SET_NULL,
    )
    language_code = models.CharField(
        max_length=35, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
    tracking_client_id = models.CharField(
        max_length=36, blank=True, editable=False)
    billing_address = models.ForeignKey(
        "accounts.Address",
        related_name="+",
        editable=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    shipping_address = models.ForeignKey(
        "accounts.Address",
        related_name="+",
        editable=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    user_email = models.EmailField(blank=True, default="")
    original = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )
    origin = models.CharField(max_length=32, choices=OrderOrigin.CHOICES)

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
    )

    # shipping_method = models.ForeignKey(
    #     ShippingMethod,
    #     blank=True,
    #     null=True,
    #     related_name="orders",
    #     on_delete=models.SET_NULL,
    # )
    # collection_point = models.ForeignKey(
    #     "warehouse.Warehouse",
    #     blank=True,
    #     null=True,
    #     related_name="orders",
    #     on_delete=models.SET_NULL,
    # )
    # shipping_method_name = models.CharField(
    #     max_length=255, null=True, default=None, blank=True, editable=False
    # )
    # collection_point_name = models.CharField(
    #     max_length=255, null=True, default=None, blank=True, editable=False
    # )

    # channel = models.ForeignKey(
    #     Channel,
    #     related_name="orders",
    #     on_delete=models.PROTECT,
    # )
    # shipping_price_net_amount = models.DecimalField(
    #     max_digits=settings.DEFAULT_MAX_DIGITS,
    #     decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    #     default=Decimal("0.0"),
    #     editable=False,
    # )
    # shipping_price_net = MoneyField(
    #     amount_field="shipping_price_net_amount", currency_field="currency"
    # )

    # shipping_price_gross_amount = models.DecimalField(
    #     max_digits=settings.DEFAULT_MAX_DIGITS,
    #     decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    #     default=Decimal("0.0"),
    #     editable=False,
    # )
    # shipping_price_gross = MoneyField(
    #     amount_field="shipping_price_gross_amount", currency_field="currency"
    # )

    # shipping_price = TaxedMoneyField(
    #     net_amount_field="shipping_price_net_amount",
    #     gross_amount_field="shipping_price_gross_amount",
    #     currency_field="currency",
    # )
    # base_shipping_price_amount = models.DecimalField(
    #     max_digits=settings.DEFAULT_MAX_DIGITS,
    #     decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    #     default=Decimal("0.0"),
    # )
    # base_shipping_price = MoneyField(
    #     amount_field="base_shipping_price_amount", currency_field="currency"
    # )
    # shipping_tax_rate = models.DecimalField(
    #     max_digits=5, decimal_places=4, blank=True, null=True
    # )
    # shipping_tax_class = models.ForeignKey(
    #     "tax.TaxClass",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )
    # shipping_tax_class_name = models.CharField(
    #     max_length=255, blank=True, null=True)
    # shipping_tax_class_private_metadata = JSONField(
    #     blank=True, null=True, default=dict,
    # )
    # shipping_tax_class_metadata = JSONField(
    #     blank=True, null=True, default=dict,
    # )

    # Token of a checkout instance that this order was created from
    checkout_token = models.CharField(max_length=36, blank=True)

    total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_total_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )

    total_net = MoneyField(amount_field="total_net_amount",
                           currency_field="currency")
    undiscounted_total_net = MoneyField(
        amount_field="undiscounted_total_net_amount", currency_field="currency"
    )

    total_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_total_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )

    total_gross = MoneyField(
        amount_field="total_gross_amount", currency_field="currency"
    )
    undiscounted_total_gross = MoneyField(
        amount_field="undiscounted_total_gross_amount", currency_field="currency"
    )

    total = TaxedMoneyField(
        net_amount_field="total_net_amount",
        gross_amount_field="total_gross_amount",
        currency_field="currency",
    )
    
    undiscounted_total = TaxedMoneyField(
        net_amount_field="undiscounted_total_net_amount",
        gross_amount_field="undiscounted_total_gross_amount",
        currency_field="currency",
    )

    total_charged_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    total_authorized_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    total_authorized = MoneyField(
        amount_field="total_authorized_amount", currency_field="currency"
    )
    total_charged = MoneyField(
        amount_field="total_charged_amount", currency_field="currency"
    )

    # voucher = models.ForeignKey(
    #     Voucher, blank=True, null=True, related_name="+", on_delete=models.SET_NULL
    # )
    # gift_cards = models.ManyToManyField(GiftCard, blank=True, related_name="orders")
    display_gross_prices = models.BooleanField(default=True)
    customer_note = models.TextField(blank=True, default="")
    # weight = MeasurementField(
    #     measurement=Weight,
    #     unit_choices=WeightUnits.CHOICES,
    #     default=zero_weight,
    # )
    redirect_url = models.URLField(blank=True, null=True)
    search_document = models.TextField(blank=True, default="")

    # this field is used only for draft/unconfirmed orders
    should_refresh_prices = models.BooleanField(default=True)
    tax_exemption = models.BooleanField(default=False)

    # class Meta:
    #     ordering = ("-number",)

    def is_fully_paid(self):
        return self.total_charged >= self.total.gross

    def is_partly_paid(self):
        return self.total_charged_amount > 0

    def get_customer_email(self):
        if self.user_id:
            return cast("User", self.user).email
        return self.user_email

    def __str__(self):
        return "#%d" % (self.id,)

    def get_subtotal(self):
        return get_subtotal(self.lines.all(), self.currency)

    def get_total_quantity(self):
        return sum([line.quantity for line in self.lines.all()])

    def is_draft(self):
        return self.status == OrderStatus.DRAFT

    def is_unconfirmed(self):
        return self.status == OrderStatus.UNCONFIRMED
    
    @property
    def total_balance(self):
        return self.total_charged - self.total.gross


class OrderLine(models.Model):
    id = models.UUIDField(primary_key=True, editable=False,
                          unique=True, default=uuid4)
    # old_id = models.PositiveIntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        Order,
        related_name="lines",
        editable=False,
        on_delete=models.CASCADE,
    )
    variant = models.ForeignKey(
        Plan,
        related_name="order_lines",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # max_length is as produced by ProductVariant's display_product method
    product_name = models.CharField(max_length=386)
    variant_name = models.CharField(max_length=255, default="", blank=True)

    product_sku = models.CharField(max_length=255, null=True, blank=True)
    # str with GraphQL ID used as fallback when product SKU is not available
    product_variant_id = models.CharField(
        max_length=255, null=True, blank=True)
    is_shipping_required = models.BooleanField(default=False)
    # is_gift_card = models.BooleanField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    quantity_fulfilled = models.IntegerField(
        validators=[MinValueValidator(0)], default=0
    )

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH, default='USD'
    )

    unit_discount_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    unit_discount = MoneyField(
        amount_field="unit_discount_amount", currency_field="currency"
    )
    # unit_discount_type = models.CharField(
    #     max_length=10,
    #     choices=DiscountValueType.CHOICES,
    #     default=DiscountValueType.FIXED,
    # )
    unit_discount_reason = models.TextField(blank=True, null=True)

    unit_price_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    # stores the value of the applied discount. Like 20 of %
    unit_discount_value = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    unit_price_net = MoneyField(
        amount_field="unit_price_net_amount", currency_field="currency"
    )

    unit_price_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    unit_price_gross = MoneyField(
        amount_field="unit_price_gross_amount", currency_field="currency"
    )

    unit_price = TaxedMoneyField(
        net_amount_field="unit_price_net_amount",
        gross_amount_field="unit_price_gross_amount",
        currency="currency",
    )

    total_price_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    total_price_net = MoneyField(
        amount_field="total_price_net_amount",
        currency_field="currency",
    )

    total_price_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    total_price_gross = MoneyField(
        amount_field="total_price_gross_amount",
        currency_field="currency",
    )

    total_price = TaxedMoneyField(
        net_amount_field="total_price_net_amount",
        gross_amount_field="total_price_gross_amount",
        currency="currency",
    )

    undiscounted_unit_price_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_unit_price_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_unit_price = TaxedMoneyField(
        net_amount_field="undiscounted_unit_price_net_amount",
        gross_amount_field="undiscounted_unit_price_gross_amount",
        currency="currency",
    )

    undiscounted_total_price_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_total_price_net_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_total_price = TaxedMoneyField(
        net_amount_field="undiscounted_total_price_net_amount",
        gross_amount_field="undiscounted_total_price_gross_amount",
        currency="currency",
    )

    base_unit_price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    base_unit_price = MoneyField(
        amount_field="base_unit_price_amount", currency_field="currency"
    )

    undiscounted_base_unit_price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=Decimal("0.0"),
    )
    undiscounted_base_unit_price = MoneyField(
        amount_field="undiscounted_base_unit_price_amount", currency_field="currency"
    )

    # tax_rate = models.DecimalField(
    #     max_digits=5, decimal_places=4, blank=True, null=True
    # )
    # tax_class = models.ForeignKey(
    #     "tax.TaxClass",
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    # )
    # tax_class_name = models.CharField(max_length=255, blank=True, null=True)
    # tax_class_private_metadata = JSONField(
    #     blank=True, null=True, default=dict,
    # )
    # tax_class_metadata = JSONField(
    #     blank=True, null=True, default=dict,
    # )

    # Fulfilled when voucher code was used for product in the line
    # voucher_code = models.CharField(max_length=255, null=True, blank=True)

    # Fulfilled when sale was applied to product in the line
    # sale_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta():
        ordering = ("created_at", "id")

    def __str__(self):
        return (
            f"{self.product_name} ({self.variant_name})"
            if self.variant_name
            else self.product_name
        )


class OrderEvent(models.Model):

    date = models.DateTimeField(default=now, editable=False)
    type = models.CharField(
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in OrderEvents.CHOICES
        ],
    )
    order = models.ForeignKey(
        Order, related_name="events", on_delete=models.CASCADE)
    parameters = JSONField(blank=True, default=dict)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    class Meta:
        ordering = ("date",)

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, user={self.user!r})"

    def __str__(self):
        return f"{self.type} - {self.user}"
