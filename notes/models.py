from django.db import models
from uuid import uuid4

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    learn = models.ForeignKey("lessons.learn", on_delete=models.DO_NOTHING, default=1)
    user = models.ForeignKey("accounts.user", on_delete=models.DO_NOTHING, default=1)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
