import math

from django.utils.timezone import now

from api.models import ChargeRule


class ChargeCalculator(object):
    def __init__(self, measurement, measurement_type, **kwargs):
        self.measurement = measurement
        self.measurement_type = measurement_type
        self.quantity = kwargs.get('quantity', 0)
        self.start_time = kwargs.get('start_time', now().timestamp())
        self.end_time = kwargs.get('end_time', now().timestamp())
        self._charge_rules = kwargs.get('rules', None)

    @property
    def charge_rules(self):
        if self._charge_rules is None:
            rules = ChargeRule.query_rules(self.measurement_type)
            self._charge_rules = rules
        return self._charge_rules

    @property
    def handled_rule(self):
        rule = self.charge_rules[0]
        # 1 credit   mcores/MB/bytes   month/day/hour/minute
        credit_unit, measurement_unit, time_unit = rule.price_unit.split(r'/')
        return credit_unit, measurement_unit, time_unit, rule.price

    def calc_with_rule(self):
        c = self.handled_rule
        if c[-2] == 'month':
            duration = math.ceil((self.end_time - self.start_time) / (60 * 60 * 24 * 30))
        elif c[-2] == 'day':
            duration = math.ceil((self.end_time - self.start_time) / (60 * 60 * 24))
        elif c[-2] == 'hour':
            duration = math.ceil((self.end_time - self.start_time) / (60 * 60))
        else:
            raise
        _fee = self.quantity * duration * c[-1]
        return _fee
