import math
import logging
import stripe
from django.db import models, connections
from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.conf import settings
from api.utils import (
    platform_credit_to_euro_cent, euro_cent_to_platform_credit,
    timestamp2datetime, next_month, RedisLock)
from api.models.fund import FundFlow, PrepaidCard
from .tax import ConsumerTaxInfo
from .base import UuidAuditedModel
from .charge import ChargeRule

logger = logging.getLogger(__name__)
User = get_user_model()
query_charge_data_sql = """
SELECT app_id, type, unit, name, cluster_id, max(usage) AS usage FROM (
    SELECT m1.app_id, m1.type, m1.unit, m1.name, m1.cluster_id, m1.usage FROM (
        SELECT
        app_id, type, unit, name, cluster_id, max(usage) AS usage
        FROM
        api_measurement
        WHERE
        owner_id={owner_id}
        AND
        usage > 0
        AND
        timestamp < {timestamp} + 3600
        AND
        timestamp >= {timestamp}
        GROUP BY app_id, type, unit, name, cluster_id
    ) AS m1
    LEFT JOIN api_measurement m2 ON
    m1.app_id=m2.app_id
    AND
    m1.type=m2.type
    AND
    m1.unit=m2.unit
    AND
    m1.usage=m2.usage
    AND
    m1.name=m2.name
    AND
    m1.cluster_id=m2.cluster_id
    UNION
    SELECT  m3.app_id, m3.type, m3.unit, m3.name, m3.cluster_id, m4.usage FROM (
        SELECT
        app_id, type, unit, name, cluster_id, max(timestamp) AS timestamp
        FROM
        api_measurement
        WHERE
        owner_id={owner_id}
        AND
        usage > 0
        AND
        type <> 'network'
        AND
        timestamp < {timestamp}
        AND
        timestamp > {timestamp} - 24 * 3600
        GROUP BY app_id, type, unit, name, cluster_id
    ) AS m3
    LEFT JOIN api_measurement m4 ON
    m3.app_id=m4.app_id
    AND
    m3.type=m4.type
    AND
    m3.unit=m4.unit
    AND
    m3.name=m4.name
    AND
    m3.timestamp=m4.timestamp
    AND
    m3.cluster_id=m4.cluster_id
) AS m5
WHERE
NOT EXISTS(
    SELECT 1 FROM api_bill AS b1
    WHERE
    b1.app_id=m5.app_id
    AND
    b1.type=m5.type
    AND
    b1.period={timestamp}
    AND
    b1.cluster_id=m5.cluster_id
)
GROUP by app_id, type, unit, name, cluster_id
"""


class Bill(UuidAuditedModel):
    app_id = models.CharField(max_length=64, db_index=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=16)
    charge = models.JSONField(default=dict)
    price = models.PositiveBigIntegerField()
    period = models.PositiveIntegerField(db_index=True)
    remark = models.TextField(null=True)
    cluster = models.ForeignKey('Cluster', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.uuid)

    @classmethod
    def bulk_create(cls, owner_id, period):
        try:
            cursor = connections['default'].cursor()
            bills = []
            for index in range(0, 24):
                timestamp = period + index * 3600
                cursor.execute(query_charge_data_sql.format(
                    owner_id=owner_id, timestamp=timestamp))
                for app_id, _type, unit, _, cluster_id, usage in cursor.fetchall():
                    rule = ChargeRule.get(_type, unit, usage, cluster_id)
                    bills.append(Bill(
                        app_id=app_id,
                        owner_id=owner_id,
                        type=_type,
                        charge=model_to_dict(rule),
                        price=rule.calc(usage),
                        period=timestamp,
                        cluster_id=cluster_id,
                    ))
            return cls.objects.bulk_create(bills)
        finally:
            connections['default'].close()

    class Meta:
        ordering = ['-created']
        unique_together = (("app_id", "type", "period"),)


class PaymentCard(UuidAuditedModel):
    PAYMENTER_PROVIDER = (
        (1, "stripe"),
    )
    name = models.CharField(max_length=128)
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    brand = models.CharField(max_length=16)
    last4 = models.CharField(max_length=4)
    line1 = models.CharField(max_length=128)
    line2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    other = models.TextField(blank=True)
    country = models.CharField(max_length=64)
    postcode = models.CharField(max_length=64, null=True, blank=True)
    exp_year = models.PositiveSmallIntegerField(db_index=True)
    exp_month = models.PositiveSmallIntegerField(db_index=True)
    extra_data = models.JSONField(blank=True)
    payment_provider = models.PositiveSmallIntegerField(choices=PAYMENTER_PROVIDER)


class Invoice(UuidAuditedModel):
    STATUS_CHOICES = [
        (0, 'Unsettled'),
        (1, 'Unpaid'),
        (2, 'Paid'),
        (3, 'No Charge'),
    ]
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    price = models.PositiveBigIntegerField()
    tax = models.PositiveBigIntegerField()
    total = models.PositiveBigIntegerField()
    paid = models.PositiveBigIntegerField()
    unpaid = models.PositiveBigIntegerField()
    period = models.PositiveIntegerField(db_index=True)
    discount = models.PositiveBigIntegerField()
    status = models.PositiveSmallIntegerField(db_index=True, choices=STATUS_CHOICES)

    @staticmethod
    def next_month_timestamp(period):
        return int(next_month(timestamp2datetime(period)).timestamp())

    @classmethod
    def calc_tax(cls, owner_id, euro_cent):
        consumer_tax_info = ConsumerTaxInfo.objects.filter(owner_id=owner_id).first()
        rate = 0 if consumer_tax_info is None else consumer_tax_info.provider["rate"]
        return math.floor(euro_cent * rate / 100)

    @classmethod
    def summary(cls, owner_id, period):
        end_timestamp = cls.next_month_timestamp(period)
        bill_sum = Bill.objects.filter(
            owner_id=owner_id, period__gte=period, period__lt=end_timestamp).order_by(
                "owner_id").values('owner_id').annotate(price=models.Sum('price'))
        if bill_sum.exists():
            assert bill_sum.count() == 1
            _, price = bill_sum.first()
            euro_cent = platform_credit_to_euro_cent(price)
            ConsumerTaxInfo.objects.filter(owner_id=owner_id).first()
            tax_euro_cent = cls.calc_tax(owner_id, euro_cent)
            if (euro_cent + tax_euro_cent) > 50:
                subtotal, tax = (
                    euro_cent_to_platform_credit(euro_cent),
                    euro_cent_to_platform_credit(tax_euro_cent))
            else:
                subtotal, tax = 0, 0
        else:
            price, subtotal, tax = 0, 0, 0
        return price, price - subtotal, tax, subtotal + tax

    @classmethod
    def create(cls, owner_id, period):
        price, discount, tax, total = cls.summary(owner_id, period)
        invoice = cls(
            owner_id=owner_id, price=price, period=period, status=1 if total > 0 else 3,
            discount=discount, tax=tax, total=total, unpaid=total
        )
        invoice.save()
        return invoice

    @property
    def bill_summary(self):
        end_timestamp = self.next_month_timestamp(self.period)
        q = models.Q(owner_id=self.owner_id, period__gte=self.period, period__lt=end_timestamp)
        return Bill.objects.filter(q).\
            order_by("app_id", "type").\
            values("app_id", "type").\
            annotate(price=models.Sum('price'))

    @property
    def payment_methods(self):
        fund_flow_list = FundFlow.objects.filter(
            direction=1,
            fund_type=1,
            trading_type=6,
            trading_id=self.uuid
        )
        return [{"remark": item.remark, "amount": item.amount} for item in fund_flow_list]

    def _pay_by_prepaid_card(self, prepaid_card):
        if prepaid_card and prepaid_card.status == 1 and prepaid_card.amount > 0:
            fund_flow = FundFlow(
                owner=self.owner, direction=1, fund_type=1, trading_type=6,
                trading_channel=1, period=self.period, trading_id=self.uuid,
                remark='platform credit payment'
            )
            if self.unpaid <= prepaid_card.amount:
                prepaid_card.amount -= self.unpaid
                fund_flow.amount = self.unpaid
                fund_flow.balance = prepaid_card.amount
                self.paid = self.unpaid
                self.unpaid = 0
                self.status = 2
            else:
                fund_flow.amount = prepaid_card.amount
                fund_flow.balance = 0
                self.paid = prepaid_card.amount
                self.unpaid -= prepaid_card.amount
                prepaid_card.amount = 0
            fund_flow.save()
            prepaid_card.save()
            self.save()

    def _pay_by_stripe(self, card):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.PaymentIntent.create(
                amount=platform_credit_to_euro_cent(self.unpaid),
                currency='eur',
                customer=card.extra_data["customer"],
                payment_method=card.extra_data["payment_method"],
                off_session=True,
                confirm=True,
                metadata={"invoice_id": self.uuid},
            )
            return True
        except stripe.error.CardError as e:
            logger.exception(e)
            payment_intent_id = e.error.payment_intent['id']
            stripe.PaymentIntent.retrieve(payment_intent_id)
        return False

    def pay(self):
        with RedisLock("paying_by_invoice:%s" % self.owner_id, ttl=600):
            if self.status == 1 and self.unpaid > 0:
                prepaid_card = PrepaidCard.objects.filter(
                    owner_id=self.owner_id, status=1).first()
                self._pay_by_prepaid_card(prepaid_card)
                if self.unpaid > 0:  # prepaid_card partially paid or unpaid
                    card = PaymentCard.objects.filter(owner=self.owner).first()
                    if card is not None:
                        if card.payment_provider == 1:  # stripe
                            return self._pay_by_stripe(card)
                        else:
                            raise NotImplementedError("this payment_provider not implemented.")
                else:  # prepaid_card pay all
                    return True
        return False

    class Meta:
        ordering = ['-created']
        unique_together = (("owner", "period"),)


class InvoiceAddress(UuidAuditedModel):
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    country = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    postcode = models.CharField(max_length=64, null=True, blank=True)
    address1 = models.CharField(max_length=128, null=True, blank=True)
    address2 = models.CharField(max_length=128, null=True, blank=True)
    other = models.TextField(null=True, blank=True)
