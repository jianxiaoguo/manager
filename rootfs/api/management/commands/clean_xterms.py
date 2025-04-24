import logging
from django.core.management.base import BaseCommand
from api.xterm import Xterm

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Last utc day of bill generation
    """

    def handle(self, *args, **options):
        Xterm.clean_all()
        self.stdout.write("done")
