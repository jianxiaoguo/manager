import logging
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from api.models.bill import Invoice
from api.tasks import block_user

User = get_user_model()
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Last utc day of bill generation
    """

    def handle(self, *args, **options):
        last_date = int((timezone.now().date() - datetime.timedelta(days=32)).timestamp())
        for owner_id, in Invoice.objects.filter(
            ~Exists(User.objects.filter(pk=OuterRef('owner_id'), status=0)),
            period__lt=last_date, status=1).order_by(
                'owner_id').distinct('owner_id').values_list("owner_id"):
            block_user.delay(owner_id)
        self.stdout.write("done")
