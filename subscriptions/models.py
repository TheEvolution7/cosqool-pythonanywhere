from django.db import models
from accounts.models import *


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(
        "plans.Plan", on_delete=models.SET_NULL, null=True, related_name="plan_subscriptions"
    )
    grade = models.ForeignKey(
        "courses.Grade", on_delete=models.SET_NULL, null=True, related_name="grade_subscriptions"
    )
    testprep = models.ForeignKey(
        "testpreps.Testprep",
        on_delete=models.SET_NULL, null=True,
        related_name="testprep_subscriptions",
    )
    option = models.ForeignKey(
        "plans.Option", on_delete=models.SET_NULL, null=True, related_name="option_subscriptions"
    )

    paypal_data = models.TextField(blank=True)
    paypal_actions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
