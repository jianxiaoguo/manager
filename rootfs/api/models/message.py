from django.db import models
from django.contrib.auth import get_user_model
from .base import UuidAuditedModel

User = get_user_model()


class Message(UuidAuditedModel):
    TYPE_CHOICES = (
        (1, 'fault'),
        (2, 'security'),
        (3, 'service'),
        (4, 'product'),
        (5, 'promotion'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    body = models.TextField(db_index=True)
    unread = models.BooleanField(default=True)
    sender = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sender")
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="receiver")

    class Meta:
        ordering = ['-created']
