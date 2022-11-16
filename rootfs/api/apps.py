from json import JSONEncoder
from uuid import UUID
from django import apps

_json_default_encoder = JSONEncoder.default
JSONEncoder.default = lambda self, obj: obj.hex \
    if isinstance(obj, UUID) else _json_default_encoder(self, obj)


class AppConfig(apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        super(AppConfig, self).ready()
        __import__("api.signals")
