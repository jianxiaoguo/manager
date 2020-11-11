import logging
from django.db import models
from api.models import UuidAuditedModel, validate_label

logger = logging.getLogger(__name__)


class Clusters(UuidAuditedModel):
    name = models.CharField(max_length=64, unique=True)
    domain = models.URLField(unique=True)
    admin = models.CharField(max_length=64)
    passwd = models.CharField(max_length=128)

