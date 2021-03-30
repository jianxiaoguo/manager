from django.db import models

from api.models import UuidAuditedModel


class Product(UuidAuditedModel):
    name = models.CharField(max_digits=63)
    resource_type = models.CharField(max_digits=63)
    describe = models.TextField(blank=True, null=True)
