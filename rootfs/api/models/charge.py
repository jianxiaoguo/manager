import math
from decimal import Decimal
from django.db import models
from django.core.cache import cache

from .base import UuidAuditedModel


class ChargeRule(UuidAuditedModel):
    """
    The billing cycle is unified as hours
    """
    name = models.CharField(max_length=64, unique=True)
    type = models.CharField(max_length=32, db_index=True)
    unit = models.CharField(max_length=32, db_index=True)
    start = models.PositiveBigIntegerField(db_index=True)
    end = models.PositiveBigIntegerField(db_index=True, null=True)
    price = models.PositiveBigIntegerField()
    group = models.PositiveBigIntegerField()
    remark = models.TextField()
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    def info(self):
        return {
            'name': self.name,
            'type': self.type,
            'unit': self.unit,
            'price': self.price,
        }

    @classmethod
    def get(cls, _type, unit, usage, cluster_id):
        key = f"charge_rules:{cluster_id}:{_type}:{unit}"
        charge_rules = cache.get_or_set(key, lambda: cls.objects.filter(
                    type=_type, unit=unit, cluster_id=cluster_id), 3600)
        for charge_rule in charge_rules:
            if charge_rule.start <= usage \
                    and (charge_rule.end is None or usage >= charge_rule.end):
                return charge_rule
        raise ValueError(
            "charge_rule not found, type={}, unit={}, usage={}, cluster_id={}".format(
                _type, unit, usage, cluster_id
            )
        )

    def calc(self, usage):
        return math.ceil(self.price * (Decimal(usage) / Decimal(self.group)))

    class Meta:
        ordering = ['-created']
        unique_together = (("start", "end", "type", "unit"),)


class ChargeUser(UuidAuditedModel):
    """
    Users participating in billing on the same day.
    """
    day = models.DateField(auto_now_add=False)
    owner_id = models.CharField(max_length=64)

    @classmethod
    def get_or_create(cls, day, owner_id):
        key = "charge_user:%s:%s" % (day, owner_id)
        return cache.get_or_set(key, lambda: cls.objects.get_or_create(
            day=day,
            owner_id=owner_id,
        ), 3600 * 12)

    class Meta:
        unique_together = (("day", "owner_id"),)
