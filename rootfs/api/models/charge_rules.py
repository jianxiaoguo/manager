from django.db import models
from django.db.models import Q

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
    # cpu:credit/mcores/day, memory:credit/MB/day, volume:credit/MB/day, network:credit/bytes/hour
    price_unit = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']

    def info(self):
        return {
            'name': self.name,
            'resource_type': self.resource_type,
            'price_unit': self.price_unit,
            'price': str(self.price),
        }

    @classmethod
    def query_rules(cls, resource_type):
        """
        :type resource_type: int
        :rtype: list
        """
        rules_q = Q(resource_type=resource_type)
        rules = ChargeRule.objects.filter(rules_q).order_by('-created')
        return list(rules)
