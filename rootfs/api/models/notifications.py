from django.conf import settings
from django.db import models

from api.models import UuidAuditedModel


class Message(UuidAuditedModel):
    codes = (
        (1, 'bill'),
        (2, 'arrearage'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    code = models.IntegerField(choices=codes, db_index=True)
    sender = models.CharField(max_length=32)
    body = models.CharField(max_length=63, db_index=True)
