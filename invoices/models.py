from django.db import models
from orders.models import *
from django.utils.timezone import now
from django.conf import settings
from django.db import models
from django.db.models import JSONField
from subscriptions.models import *


class JobStatus:
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    DELETED = "deleted"

    CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (DELETED, "Deleted"),
    ]


class InvoiceEvents:
    REQUESTED = "requested"
    REQUESTED_DELETION = "requested_deletion"
    CREATED = "created"
    DELETED = "deleted"
    SENT = "sent"

    CHOICES = [
        (REQUESTED, "The invoice was requested"),
        (REQUESTED_DELETION, "The invoice was requested for deletion"),
        (CREATED, "The invoice was created"),
        (DELETED, "The invoice was deleted"),
        (SENT, "The invoice has been sent"),
    ]


class InvoiceQueryset(models.QuerySet["Invoice"]):
    def ready(self):
        return self.filter(job__status=JobStatus.SUCCESS)


InvoiceManager = models.Manager.from_queryset(InvoiceQueryset)


class Invoice(models.Model):
    # order = models.ForeignKey(
    #     Order,
    #     related_name="invoices",
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )
    subscription = models.ForeignKey(
        Subscription,
        related_name="subscriptions",
        null=True,
        on_delete=models.SET_NULL,
    )
    number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created = models.DateTimeField(null=True)
    external_url = models.URLField(null=True, max_length=2048, blank=True)
    invoice_file = models.FileField(upload_to="invoices", blank=True)

    objects = InvoiceManager()

    status = models.CharField(
        max_length=50, choices=JobStatus.CHOICES, default=JobStatus.PENDING
    )
    message = models.TextField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_invoice(self, number=None, url=None):
        if number is not None:
            self.number = number
        if url is not None:
            self.external_url = url

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        out = self.id
        if self.number is not None:
            out = self.number
        return f"Invoice #{out}"


class InvoiceEvent(models.Model):
    date = models.DateTimeField(default=now, editable=False)
    type = models.CharField(max_length=255, choices=InvoiceEvents.CHOICES)
    invoice = models.ForeignKey(
        Invoice, related_name="events", blank=True, null=True, on_delete=models.SET_NULL
    )
    # order = models.ForeignKey(
    #     Order,
    #     related_name="invoice_events",
    #     blank=True,
    #     null=True,
    #     on_delete=models.SET_NULL,
    # )

    subscription = models.ForeignKey(
        Subscription,
        related_name="subscriptions_events",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    parameters = JSONField(blank=True, default=dict)

    class Meta:
        ordering = ("date", "pk")

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, user={self.user!r})"
    
