from django.conf import settings
from django.db import models

from api.models import UuidAuditedModel


class Bill(UuidAuditedModel):
    resource_types = (
        (1, 'cpu'),
        (2, 'memory'),
        (3, 'volume'),
        (4, 'network'),

    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT)
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)
    app_id = models.CharField(max_length=63, db_index=True)
    resource_type = models.IntegerField(choices=resource_types, db_index=True)
    price_unit = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
