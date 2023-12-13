from django.db import models
from accounts.models import *
from django.utils import timezone
import datetime
from courses.models import Grade
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey("plans.Plan", on_delete=models.DO_NOTHING)
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True, blank=True)
    testprep = models.ForeignKey("testpreps.Testprep", on_delete=models.DO_NOTHING, null=True, blank=True)
    option = models.ForeignKey("plans.Option", on_delete=models.DO_NOTHING)
    
    paypal_data = models.TextField(blank=True)
    paypal_actions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
