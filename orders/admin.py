from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django import forms
from django.forms import ModelForm
from django.urls import path
from django.template.response import TemplateResponse
from core.admin import *

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ('product_name', 'quantity', 'unit_price_gross_amount', 'total_price_gross_amount', )


class OrderEventInline(admin.TabularInline):
    model = OrderEvent
    extra = 0
    can_delete = False
    fields = ('type', 'user', )


class OrderForm(ModelForm):
    status = forms.CharField(
        required=False,
        widget=forms.Select(attrs={'data-control': "select2"}))

    class Meta:
        model = Order
        fields = '__all__'


def action_tag(self, obj):
    return mark_safe(f'<div class="sweetalert"><div class="d-flex justify-content-end"><a href="{obj.id}/view" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="View"><i class="fa fa-eye"></i></a><a href="{obj.id}/change" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Edit"><i class="fa fa-pencil"></i></a><a href="{obj.id}/delete" class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1" title="Delete"><i class="fa fa-trash"></i></a></div></div>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date', 'customer', 'total_tag',
                    'payment_status', 'items', 'action_tag', ]

    @admin.display(description=_('date'))
    def date(self, obj):
        return f"{obj.created_at.strftime('%b %M %Y at %I:%M %p')}"

    @admin.display(description=_('customer'))
    def customer(self, obj):
        return f"{obj.user}"

    @admin.display(description=_('total'))
    def total_tag(self, obj):
        currency = "{:,.2f}".format(obj.total_charged_amount)
        return f"{obj.currency} {currency}"

    @admin.display(description=_('payment status'))
    def payment_status(self, obj):
        out = _('UnPaid')
        if obj.is_partly_paid():
            out = _('Paid')
        return mark_safe('<span class="badge badge-primary">'+out+'</span>')

    @admin.display(description=_('items'))
    def items(self, obj):
        return _(f"{obj.lines.count()} item")

    @admin.display(description='action')
    def action_tag(self, obj):
        return action_tag(self, obj)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<path:object_id>/view/', self.admin_site.admin_view(self.view,
                 cacheable=True), name='orders_order_view')
        ]

        return my_urls + urls

    def view(self, request, object_id):
        context = dict(
            self.admin_site.each_context(request),
        )
        context.update({'order': Order.objects.filter(pk=object_id).first()})
        return TemplateResponse(request, "admin/view.html", context)

    # change_form_template = 'admin/change_form_orders.html'
    fieldsets = (
        (None, {
            'fields': (
                ('user_email', 'user', 'original', 'origin'),
                ('status', 'authorize_status', 'charge_status', ),
                ('language_code', 'currency', 'checkout_token'),
                ('total_net_amount', 'undiscounted_total_net_amount'),
                ('total_gross_amount', 'undiscounted_total_gross_amount'),
                ('total_charged_amount', 'total_authorized_amount', ),
                ('should_refresh_prices', 'tax_exemption', 'redirect_url', ),
                'customer_note',
            )
        }),
        (_('Order Details'), {
            'fields': ('billing_address', 'shipping_address', ),
        }),
    )
    inlines = [OrderLineInline, OrderEventInline]
    readonly_fields = ('currency', 'checkout_token', 'total_net_amount', 'undiscounted_total_net_amount', 'total_gross_amount',
                       'undiscounted_total_gross_amount', 'redirect_url', 'total_charged_amount', 'total_authorized_amount',)

@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'product_sku', 'quantity',
                    'undiscounted_base_unit_price_amount', 'base_unit_price_amount', )
    fieldsets = (
        (None, {
            'fields': ('product_name', 'variant_name', 'product_sku', ('quantity', 'currency'), ('unit_discount_amount', 'unit_discount_value'), 'unit_discount_reason', ('undiscounted_unit_price_net_amount', 'undiscounted_total_price_net_amount'), ('undiscounted_unit_price_gross_amount', 'undiscounted_total_price_gross_amount'), )
        }),
        (_('Price Gross'), {
            'fields': ('unit_price_gross_amount', 'total_price_gross_amount', ),
        }),
        (_('Price Net'), {
            'fields': ('unit_price_net_amount', 'total_price_net_amount', ),
        }),
        (_('Unit Price'), {
            'fields': ('base_unit_price_amount', 'undiscounted_base_unit_price_amount', ),
        }),
    )


@admin.register(OrderEvent)
class OrderEventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('type', 'parameters', )
        }),
        (_('Order'), {
            'fields': ('order', ),
        }),
        (_('User'), {
            'fields': ('user', ),
        }),
    )
