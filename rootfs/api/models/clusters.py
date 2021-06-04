import logging
from django.db import models
from api.models import UuidAuditedModel

logger = logging.getLogger(__name__)


class Cluster(UuidAuditedModel):
    """
    the kubernetes cluster drycc info, config LDAP superuser drycc
    """
    name = models.CharField(max_length=64, unique=True)
    ingress = models.URLField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
