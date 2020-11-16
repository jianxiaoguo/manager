import logging
from django.db import models
from api.models import UuidAuditedModel

logger = logging.getLogger(__name__)


class Cluster(UuidAuditedModel):
    """
    the kubernetes cluster drycc info, config LDAP superuser\influxdb\drycc
    """
    name = models.CharField(max_length=64, unique=True)
    admin = models.CharField(max_length=64)
    passwd = models.CharField(max_length=128)
    drycc_ingress = models.URLField(unique=True)
    influxdb_ingress = models.URLField(unique=True, required=False)
