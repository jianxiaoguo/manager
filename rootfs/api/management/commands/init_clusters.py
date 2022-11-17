import uuid
import json
import pathlib
from django.core.management.base import BaseCommand
from api.models.cluster import Cluster


class Command(BaseCommand):
    """Management command for init clusters"""

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument(
            '--path', dest='path', default=None,
            help='Specifies the path for the secret.',
        )

    def handle(self, *args, **options):
        base_path = options.get('path', '')
        for item in json.loads(pathlib.Path(base_path).read_text()):
            _, updated = Cluster.objects.update_or_create(
                uuid=uuid.UUID(item["key"]),
                defaults={
                    'name': item["name"],
                    'url': item["url"],
                    'secret': item["secret"],
                }
            )
            if updated:
                self.stdout.write('Drycc %s cluster created' % item["name"])
            else:
                self.stdout.write('Drycc %s cluster updated' % item["name"])
