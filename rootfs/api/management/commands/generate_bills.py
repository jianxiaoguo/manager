import logging
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from api.tasks import generate_bill
from api.models.charge import ChargeUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Last utc day of bill generation
    """

    def handle(self, *args, **options):
        bill_date = timezone.now().date() - datetime.timedelta(days=1)
        for owner_id, in ChargeUser.objects.filter(day=bill_date).values_list('owner_id'):
            generate_bill.delay(owner_id, bill_date)
        self.stdout.write("done")
