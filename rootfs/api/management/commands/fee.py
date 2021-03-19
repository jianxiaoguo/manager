import logging
from django.core.management.base import BaseCommand
from django.conf import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # 1 计费(每个资源的计费)
        # 2 生成账单\收支明细
        # 3 通知message
        self.stdout.write("done")
