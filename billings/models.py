from django.db import models
from accounts.models import User
from django.utils.translation import gettext_lazy as _

class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    email = models.EmailField()
    
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Billing")
        verbose_name_plural = _("Billings")
        
class BillingItem(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.DO_NOTHING)
    plan = models.ForeignKey("plans.Plan", on_delete=models.DO_NOTHING)
    