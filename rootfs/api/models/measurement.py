import logging
from django.db import models
from django.conf import settings
from .base import UuidAuditedModel

logger = logging.getLogger(__name__)


class Measurement(UuidAuditedModel):
    app_id = models.CharField(max_length=64, db_index=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    unit = models.CharField(max_length=16)
    usage = models.PositiveBigIntegerField(db_index=True)
    timestamp = models.PositiveIntegerField(db_index=True)
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)

    class Meta:
        ordering = ['-timestamp']
