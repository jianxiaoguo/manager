import logging
import datetime
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from api.models.fund import PrepaidCard, FundFlow
from api.models.measurement import Measurement
from api.tasks import generate_charge_user, supplementary_payment

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def user_changed_handle(sender, instance=None, created=False, update_fields=None, **kwargs):
    if created:
        PrepaidCard(
            owner=instance,
            status=2,
            amount=0,
            remark="init prepaid card"
        ).save()
    else:
        logger.debug(f"User {instance.username} changed.")


@receiver(post_save, sender=Measurement)
def measurement_changed_handle(sender, instance=None, created=False, update_fields=None, **kwargs):
    if instance.usage > 0:
        date = datetime.datetime.utcfromtimestamp(instance.timestamp)
        date.replace(tzinfo=timezone.get_default_timezone())
        generate_charge_user.delay(date, instance.owner_id)
    else:
        logger.debug(
            f"The measurement with {instance.id}:{instance.type}:{instance.name} is not used")


@receiver(post_save, sender=FundFlow)
def fund_flow_changed_handle(sender, instance=None, created=False, update_fields=None, **kwargs):
    if created and instance.trading_type != 6:
        supplementary_payment.delay(instance.owner_id)
        logger.debug(f"User id {instance.owner_id}, new prepaid card have been recorded.")
    else:
        logger.debug(f"User id {instance.owner_id}, the prepaid card amount has changed.")
