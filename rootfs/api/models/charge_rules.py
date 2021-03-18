from django.db import models
from api.models import UuidAuditedModel


class ChargeRule(UuidAuditedModel):
    resource_types = (
        (1, 'cpu'),
        (2, 'memory'),
        (3, 'volume'),
        (4, 'network'),
    )
    name = models.CharField(max_length=64, unique=True)
    resource_type = models.IntegerField(choices=resource_types, db_index=True)
    price_unit = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name
