import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.utils import last_month
from api.tasks import generate_invoice

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Last utc day of invoice generation
    """

    def handle(self, *args, **options):
        invoice_date = last_month(timezone.now()).date()
        if invoice_date.day < 29:
            for user_id, in User.objects.filter(invoice_day=invoice_date.day).values_list("pk"):
                generate_invoice.delay(user_id, invoice_date)
        self.stdout.write("done")
