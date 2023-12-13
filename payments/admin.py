from django.contrib import admin
from .models import *

@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    pass

@admin.register(TransactionEvent)
class TransactionEventAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
