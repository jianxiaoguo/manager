from django.db import models
from django.contrib.auth import get_user_model
from .base import UuidAuditedModel

User = get_user_model()


class FundFlow(UuidAuditedModel):
    DIRECTION_CHOICES = (
        (1, 'income'),
        (2, 'expense'),
    )
    FUND_TYPE = (
        (1, 'cash'),
        (2, 'order online payment'),
    )
    TRADING_TYPE_CHOICES = (
        (1, 'account adjustment'),
        (2, 'recharge'),
        (4, 'refund'),
        (5, 'withdrawal'),
        (6, 'consumption'),
    )
    TRADING_CHANNEL_CHOICES = (
        (1, 'user blance'),
        (2, 'bank transfer'),
        (3, 'alipay'),
        (4, 'wechat'),
        (5, 'offline remittance'),
        (6, 'credit card'),
    )
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    direction = models.PositiveSmallIntegerField(choices=DIRECTION_CHOICES)
    fund_type = models.PositiveSmallIntegerField(choices=FUND_TYPE)
    trading_id = models.CharField(null=True, max_length=128)
    trading_type = models.PositiveSmallIntegerField(choices=TRADING_TYPE_CHOICES)
    trading_channel = models.PositiveSmallIntegerField(choices=TRADING_CHANNEL_CHOICES)
    trading_channel_id = models.CharField(null=True, max_length=128)
    associated_account_id = models.CharField(null=True, max_length=128)
    period = models.PositiveIntegerField(db_index=True)
    amount = models.PositiveBigIntegerField(db_index=True)
    balance = models.PositiveBigIntegerField(db_index=True)
    remark = models.TextField(null=True)

    class Meta:
        ordering = ['-created']


class PrepaidCard(UuidAuditedModel):
    STATUS_CHOICES = (
        (1, "normal"),
        (2, "frozen")
    )
    owner = models.OneToOneField(User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    remark = models.TextField(null=True)
