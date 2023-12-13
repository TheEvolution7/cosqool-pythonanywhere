from django.contrib import admin
from .models import *

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    pass

@admin.register(CheckoutLine)
class CheckoutLineAdmin(admin.ModelAdmin):
    pass

@admin.register(CheckoutMetadata)
class CheckoutMetadataAdmin(admin.ModelAdmin):
    pass

