import logging
import base64
from django.db import models
from api.utils import generate_secret
from .base import UuidAuditedModel

logger = logging.getLogger(__name__)


class Cluster(UuidAuditedModel):
    """
    the kubernetes cluster drycc info, config LDAP superuser drycc
    """
    name = models.CharField(max_length=64, unique=True)
    url = models.URLField(unique=True)
    secret = models.CharField(default=generate_secret, max_length=64, auto_created=True)

    @property
    def token(self):
        return base64.b85encode(b"%s:%s" % (
            str(self.uuid).encode("utf8"),
            self.secret.encode("utf8"),
        )).decode("utf8")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
