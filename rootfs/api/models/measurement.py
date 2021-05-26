import json
import logging
import uuid

from django.db import models

from api.charge_calculator import ChargeCalculator
from api.models import UuidAuditedModel, ChargeRule, Bill, Funding
from api.utils import get_user_by_name, timestamp2datetime

logger = logging.getLogger(__name__)


class MeasurementModel(UuidAuditedModel):
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)
    app_id = models.CharField(max_length=63, db_index=True)
    owner_id = models.CharField(max_length=63, db_index=True)
    timestamp = models.FloatField(db_index=True)

    class Meta:
        """Mark :class:`MeasurementModel` as abstract."""
        abstract = True
        ordering = ['-timestamp']


class Config(MeasurementModel):
    container_type = models.CharField(max_length=63)
    cpu = models.PositiveIntegerField()
    memory = models.PositiveIntegerField()

    def info(self, resource_type):
        res = {'container_type': self.container_type}
        if resource_type == 1:
            res.update({'cpu': self.cpu,})
        elif resource_type == 2:
            res.update({'memory': self.memory,})
        return res


class Volume(MeasurementModel):
    name = models.CharField(max_length=63)
    size = models.PositiveIntegerField()

    def info(self):
        return {
            'name': self.name,
            'size': self.size,
        }

class Network(MeasurementModel):
    pod_name = models.CharField(max_length=63)
    rx_bytes = models.PositiveIntegerField()
    tx_bytes = models.PositiveIntegerField()

    def info(self):
        return {
            'pod_name': self.pod_name,
            'rx_bytes': self.rx_bytes,
            'tx_bytes': self.tx_bytes,
        }

class Instance(MeasurementModel):
    container_type = models.CharField(max_length=63)
    container_count = models.PositiveIntegerField()

    def info(self):
        return {
            'container_type': self.container_type,
            'container_count': self.container_count,
        }

class Resource(MeasurementModel):
    name = models.CharField(max_length=63)
    plan = models.CharField(max_length=128)

    def info(self):
        return {
            'name': self.name,
            'plan': self.plan,
        }

def config_fee(i, start, end):
    cs = Config.objects.filter(cluster_id=i[0], owner_id=i[1],
                               app_id=i[2], timestamp__gte=start,
                               timestamp__lt=end)
    owner_id = get_user_by_name(i[1]).id
    try:
        credit = Funding.objects.filter(owner_id=owner_id). \
            latest('created').credit
    except Funding.DoesNotExist:
        credit = 0
    _rule_cpu = ChargeRule.query_rules(1)
    _rule_mem = ChargeRule.query_rules(2)
    _charge_fee(i, cs, credit, _rule_mem, start, end)
    credit = Funding.objects.filter(owner_id=owner_id).latest('created').credit
    _charge_fee(i, cs, credit, _rule_cpu, start, end)


def volume_fee(instance, start, end):
    vs = Volume.objects.filter(cluster_id=instance[0], owner_id=instance[1],
                               app_id=instance[2], timestamp__gte=start,
                               timestamp__lt=end)
    owner_id = get_user_by_name(instance[1]).id
    try:
        credit = Funding.objects.filter(owner_id=owner_id). \
            latest('created').credit
    except Funding.DoesNotExist:
        credit = 0
    _rule_volume = ChargeRule.query_rules(3)
    _charge_fee(instance, vs, credit, _rule_volume, start, end)


def network_fee(instance, start, end):
    ns = Network.objects.filter(cluster_id=instance[0], owner_id=instance[1],
                                app_id=instance[2], timestamp__gte=start,
                                timestamp__lt=end)
    owner_id = get_user_by_name(instance[1]).id
    try:
        credit = Funding.objects.filter(owner_id=owner_id). \
            latest('created').credit
    except Funding.DoesNotExist:
        credit = 0
    _rule_volume = ChargeRule.query_rules(3)
    _charge_fee(instance, ns, credit, _rule_volume, start, end)


def _charge_fee(instance, resources, credit, _rule, start, end):
    owner_id = get_user_by_name(instance[1]).id
    bills = []
    fundings = []
    for r in resources:
        quantity = {1: "r.cpu", 2: "r.memory", 3: "r.size",
                    4: "r.rx_bytes" + "r.tx_bytes", 5: "r.plan"}
        resource_quantity = eval(quantity[_rule[0].resource_type])
        _fee = ChargeCalculator(r, 1, start_time=start, end_time=end,
            rules=_rule, quantity=resource_quantity).calc_with_rule()
        bill_id = uuid.uuid4()
        resource_info = r.info(_rule[0].resource_type) if \
                _rule[0].resource_type in [1, 2] else r.info()
        bill_data = {
            'uuid': bill_id,
            'resource_type': _rule[0].resource_type,
            'cluster_id': instance[0],
            'app_id': instance[2],
            'owner_id': owner_id,
            # 'price_unit': _rule[0].price_unit,
            # 'price': _rule[0].price,
            'charge_rule_info': _rule[0].info(),
            'resource_info': resource_info,
            'total_price': _fee,
            'start_time': timestamp2datetime(start),
            'end_time': timestamp2datetime(end)
        }
        bills.append(Bill(**bill_data))

        credit -= _fee
        funding_data = {
            'trade_type': 1,
            'owner_id': owner_id,
            'operator': 'system',
            'bill_id': bill_id,
            'trade_credit': _fee,
            'credit': credit,
            'remark': ' paid by the day'
        }
        fundings.append(Funding(**funding_data))
    # create bill funding
    Bill.objects.bulk_create(bills)
    Funding.objects.bulk_create(fundings)
