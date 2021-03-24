import logging

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.timezone import now

from api.models import Instance
from api.models.measurement import config_fee, volume_fee, network_fee
from api.utils import date2timestamp

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        end = date2timestamp(now().date())
        start = end - 86400
        instances = Instance.objects.values_list('cluster_id', 'owner_id', 'app_id'). \
            filter(timestamp__gte=start, timestamp__lt=end).order_by('owner_id'). \
            annotate(Count('app_id'))
        for instance in instances:
            config_fee(instance, start, end)
            volume_fee(instance, start, end)
            network_fee(instance, start, end)
        self.stdout.write("done")
