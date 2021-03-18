from django.conf import settings
from django.db import models
from jsonfield import JSONField

from api.models import UuidAuditedModel


class Funding(UuidAuditedModel):
    trade_types = (
        (1, 'expend'),
        (2, 'income'),

    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.PROTECT)
    operator = models.CharField(max_length=63)
    # cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT, null=True, blank=True)
    # app_id = models.CharField(max_length=63, db_index=True)
    billing = models.ForeignKey('Bill', on_delete=models.PROTECT, null=True,
                                blank=True)
    credit = models.DecimalField(max_digits=12, decimal_places=2)
    # expend\income
    trade_type = models.IntegerField(choices=trade_types, db_index=True)
    trade_credit = models.DecimalField(max_digits=12, decimal_places=2)
    remark = models.TextField(blank=True, null=True)
